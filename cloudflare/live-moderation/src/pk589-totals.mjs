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
    const [all,numbered,gifts]=await Promise.all([
      aggregate('reactions',[{alias:'all',count:{}}]),
      aggregate('reactions',[{alias:'numbered',count:{}},{alias:'likes',sum:{field:{fieldPath:'count'}}}],
        {fieldFilter:{field:{fieldPath:'count'},op:'GREATER_THAN_OR_EQUAL',value:{integerValue:'0'}}}),
      aggregate('comments',[{alias:'gifts',sum:{field:{fieldPath:'points'}}}],
        {fieldFilter:{field:{fieldPath:'kind'},op:'EQUAL',value:{stringValue:'gift'}}}),
    ]);
    // Legacy reaction documents had no count; each represented one heart.
    const legacy=total(all.all)-total(numbered.numbered);
    const likes=total(numbered.likes)+legacy,giftPoints=total(gifts.gifts);
    if(legacy<0||!Number.isSafeInteger(likes))throw Error('invalid_score_snapshot');
    return {likeCount:likes,giftPoints};
  };
}
