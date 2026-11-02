import {decode} from '../../call-push/src/google.mjs';

const validId=value=>typeof value==='string'&&/^[A-Za-z0-9_-]{1,160}$/.test(value);
const total=value=>{
  const number=decode(value);
  if(!Number.isSafeInteger(number)||number<0)throw Error('invalid_score_snapshot');
  return number;
};
export function pkTotals589(api){
  if(typeof api!=='function')throw Error('Score snapshot API required');
  return async(liveId,at)=>{
    if(!validId(liveId)||!Number.isSafeInteger(at)||at<0)throw Error('invalid_score_snapshot');
    const readTime=new Date(at).toISOString();
    async function aggregate(collection,aggregations,where){
      const rows=await api('/live_streams/'+liveId+':runAggregationQuery',{
        structuredAggregationQuery:{structuredQuery:{from:[{collectionId:collection}],...(where?{where}:{})},aggregations},readTime});
      if(!Array.isArray(rows)||rows.length!==1||!rows[0].result?.aggregateFields)throw Error('invalid_score_snapshot');
      return rows[0].result.aggregateFields;
    }
    async function giftTotal(){
      // A single-field kind query needs no composite index. Project only points;
      // bounded reads fail closed instead of silently returning a partial score.
      const rows=await api('/live_streams/'+liveId+':runQuery',{
        structuredQuery:{select:{fields:[{fieldPath:'points'}]},from:[{collectionId:'comments'}],
          where:{fieldFilter:{field:{fieldPath:'kind'},op:'EQUAL',value:{stringValue:'gift'}}},limit:20001},readTime});
      if(!Array.isArray(rows)||!rows.length)throw Error('invalid_score_snapshot');
      let sum=0,count=0;
      for(const row of rows){
        if(row.document){
          if(++count>20000)throw Error('score_snapshot_too_large');
          sum+=total(row.document.fields?.points);
          if(!Number.isSafeInteger(sum))throw Error('invalid_score_snapshot');
        }else if(!row.readTime)throw Error('invalid_score_snapshot');
      }
      return sum;
    }
    const [all,numbered,gifts]=await Promise.all([
      aggregate('reactions',[{alias:'all',count:{}}]),
      aggregate('reactions',[{alias:'numbered',count:{}},{alias:'likes',sum:{field:{fieldPath:'count'}}}],
        {fieldFilter:{field:{fieldPath:'count'},op:'GREATER_THAN_OR_EQUAL',value:{integerValue:'0'}}}),
      giftTotal(),
    ]);
    // Legacy reaction documents had no count; each represented one heart.
    const legacy=total(all.all)-total(numbered.numbered);
    const likes=total(numbered.likes)+legacy,giftPoints=gifts;
    if(legacy<0||!Number.isSafeInteger(likes))throw Error('invalid_score_snapshot');
    return {likeCount:likes,giftPoints};
  };
}
