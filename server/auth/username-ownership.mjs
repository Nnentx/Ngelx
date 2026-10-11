import {parseIdentifier} from './identifier-login.mjs';

const reserved = new Set(['admin','administrator','ngelx','support','destek',
  'moderator','root','official','resmi']);
export class UsernameFailure extends Error {
  constructor(code) { super(code); this.code=code; }
}
export function normalizeUsername(raw) {
  let parsed;
  try { parsed=parseIdentifier(raw); } catch { throw new UsernameFailure('invalid-username'); }
  if(parsed.kind!=='username'||reserved.has(parsed.value)) {
    throw new UsernameFailure('invalid-username');
  }
  return parsed.value;
}

// SERVER ONLY. authenticatedUid must come from verified Auth, never request body.
// Enable only with coordinated rules that prohibit direct profile username edits.
export async function claimUsername(db, authenticatedUid, raw) {
  if(typeof authenticatedUid!=='string'||!authenticatedUid||authenticatedUid.includes('/')||authenticatedUid.length>128) {
    throw new UsernameFailure('unauthenticated');
  }
  const name=normalizeUsername(raw);
  const profileRef=db.collection('users').doc(authenticatedUid);
  const targetRef=db.collection('login_usernames').doc(name);
  return db.runTransaction(async tx=>{
    const profile=await tx.get(profileRef);
    if(!profile.exists)throw new UsernameFailure('profile-required');
    const old=profile.data()?.usernameLower;
    const target=await tx.get(targetRef);
    // Legacy accounts may not have an index yet. Never award their name to a
    // newer caller; check existing profiles during the transition.
    const legacy=await tx.get(db.collection('users').where('usernameLower','==',name).limit(2));
    if(legacy.docs.some(doc=>doc.id!==authenticatedUid))throw new UsernameFailure('username-taken');
    const record=target.data();
    if(target.exists&&(record?.status!=='active'||record?.uid!==authenticatedUid)) {
      throw new UsernameFailure('username-taken');
    }
    let oldRef,oldRecord;
    if(typeof old==='string'&&old!==name&&/^[a-z0-9._]{3,20}$/.test(old)) {
      oldRef=db.collection('login_usernames').doc(old);
      oldRecord=await tx.get(oldRef);
      if(oldRecord.exists&&(oldRecord.data()?.uid!==authenticatedUid||oldRecord.data()?.status!=='active')) {
        throw new UsernameFailure('ownership-conflict');
      }
    }
    // All reads finished. Atomic ownership and profile update preserve other
    // fields. Retire the old name instead of exposing immediate impersonation.
    tx.set(targetRef,{uid:authenticatedUid,status:'active',version:1});
    tx.update(profileRef,{username:raw.trim(),usernameLower:name});
    if(oldRef)tx.set(oldRef,{uid:authenticatedUid,status:'retired',version:1});
    return {username:raw.trim(),usernameLower:name};
  });
}

// Read-only migration planning. Caller must provide a complete consistent
// profile snapshot; applying this result without revalidation is forbidden.
export function planUsernameMigration(profiles) {
  const groups=new Map();const invalid=[];
  for(const profile of profiles){
    let name;
    try {
      name=normalizeUsername(profile.usernameLower);
      if(name!==profile.usernameLower||typeof profile.uid!=='string'||!profile.uid)throw Error();
    }catch{invalid.push({uid:profile.uid,reason:'invalid-username'});continue;}
    const ids=groups.get(name)||new Set();ids.add(profile.uid);groups.set(name,ids);
  }
  const active=[],conflicts=[];
  for(const [username,ids] of [...groups].sort(([a],[b])=>a.localeCompare(b))){
    if(ids.size===1)active.push({username,uid:[...ids][0]});
    else conflicts.push({username,uids:[...ids].sort()});
  }
  return {active,conflicts,invalid};
}
