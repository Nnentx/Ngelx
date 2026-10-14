export function scheduledOutcome(community,post,now){
 if(!community||!post||post.status!=='scheduled')return 'ignore';
 if(!Number.isFinite(post.publishAt)||post.publishAt>now+2000)return 'retry';
 if(community.paused||!community.members?.includes(post.authorId)||!community.admins?.includes(post.authorId)||community.muted?.includes(post.authorId)||community.banned?.includes(post.authorId))return 'reject';
 return 'publish';
}
