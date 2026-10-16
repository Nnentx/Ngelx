#!/usr/bin/env python3
"""Build465 device follow-up: recover stalled, UID-bound private inbox profiles.

Run only after the existing Build457 identity/row patches, then Build464.
No Firestore writes, rule changes, migration or production service calls.
Fail closed if the generated inbox structure has changed.
"""
from pathlib import Path
import re

MAIN = Path("app/lib/main.dart")
STATE = "class _MesajPageState extends State<MesajPage> {"
FIELD = "  String? get uid=>FirebaseAuth.instance.currentUser?.uid;"
DISPOSE = "  @override void dispose(){sohbetAra.dispose();super.dispose();}"
OLD = """if(u.hasError)return ListTile(
                        title:const Text('Kişi bilgisi yüklenemedi'),
                        trailing:IconButton(
                          onPressed:()=>setState(()=>_profiles453.remove(other)),
                          icon:const Icon(Icons.refresh_rounded),
                        ),
                      );
                      if(!u.hasData)return const ListTile(
                        title:Text('Kişi bilgisi yükleniyor…'),
                        leading:CircleAvatar(child:Icon(Icons.person_outline)),
                      );
                      if(u.data!.id!=other)return const SizedBox.shrink();"""
NEW = """if(u.hasError){
                        _ngelx465PlanProfileRetry(other);
                        return ListTile(
                          title:const Text('Kişi bilgisi yüklenemedi'),
                          trailing:IconButton(
                            tooltip:'Kişiyi yeniden yükle',
                            onPressed:()=>_ngelx465RetryProfileNow(other),
                            icon:const Icon(Icons.refresh_rounded),
                          ),
                        );
                      }
                      if(!u.hasData){
                        _ngelx465PlanProfileRetry(other);
                        if((_ngelx465ProfileRetryCount[other]??0)>=3){
                          return ListTile(
                            title:const Text('Kişi bilgisi alınamadı'),
                            trailing:IconButton(
                              tooltip:'Kişiyi yeniden yükle',
                              onPressed:()=>_ngelx465RetryProfileNow(other),
                              icon:const Icon(Icons.refresh_rounded),
                            ),
                          );
                        }
                        return const ListTile(
                          title:Text('Kişi bilgisi yükleniyor…'),
                          leading:CircleAvatar(child:Icon(Icons.person_outline)),
                        );
                      }
                      if(u.data!.id!=other)return const SizedBox.shrink();
                      _ngelx465ProfileResolved(other);"""
WATCHDOG = """  // Build466 inbox retry watchdog: bounded, per-UID and local only.
  final Map<String,Timer> _ngelx465ProfileRetryTimers={};
  final Map<String,int> _ngelx465ProfileRetryCount={};
  void _ngelx465PlanProfileRetry(String target){
    if(_ngelx465ProfileRetryTimers.containsKey(target))return;
    final retry=_ngelx465ProfileRetryCount[target]??0;
    if(retry>=3)return;
    final account=FirebaseAuth.instance.currentUser?.uid;
    if(account==null)return;
    _ngelx465ProfileRetryTimers[target]=Timer(Duration(seconds:5*(retry+1)),(){
      _ngelx465ProfileRetryTimers.remove(target);
      if(!mounted||FirebaseAuth.instance.currentUser?.uid!=account)return;
      _ngelx465ProfileRetryCount[target]=retry+1;
      // Re-create only this recipient's stream; do not recycle another row.
      setState(()=>_profiles453.remove(target));
    });
  }
  void _ngelx465ProfileResolved(String target){
    _ngelx465ProfileRetryTimers.remove(target)?.cancel();
    _ngelx465ProfileRetryCount.remove(target);
  }
  void _ngelx465RetryProfileNow(String target){
    _ngelx465ProfileResolved(target);
    if(mounted)setState(()=>_profiles453.remove(target));
  }
"""
def replace_one(s: str, old: str, new: str, what: str) -> str:
    n=s.count(old)
    if n!=1:
        raise RuntimeError(f"Build465 inbox recovery: expected one {what}, found {n}")
    return s.replace(old,new,1)

def transform(source: str) -> str:
    if "// Build466 inbox retry watchdog" in source:
        return source
    begin=source.index(STATE)
    end=source.index("class ArsivSohbetlerPage",begin)
    region=source[begin:end]
    if "_profiles453.putIfAbsent(other" not in region:
        raise RuntimeError("Expected existing UID-bound profile stream not found")
    region=replace_one(region,FIELD,WATCHDOG+FIELD,"state field")
    region=replace_one(region,OLD,NEW,"Build457 error/loading guard")
    dispose=list(re.finditer(r"@override\\s+void\\s+dispose\\s*\\(\\s*\\)\\s*\\{",region))
    if len(dispose)!=1:
        raise RuntimeError(
            "Build465 inbox recovery: expected one inbox dispose, found "
            +str(len(dispose))+"; occurrences of dispose: "
            +str(region.count("dispose("))
        )
    pos=dispose[0].end()
    region=region[:pos]+"""
    for(final t in _ngelx465ProfileRetryTimers.values){t.cancel();}
    _ngelx465ProfileRetryTimers.clear();
    """+region[pos:]
    return source[:begin]+region+source[end:]

def main():
    before=MAIN.read_text(encoding="utf-8")
    after=transform(before)
    if before!=after: MAIN.write_text(after,encoding="utf-8")
    print("Build465 device feedback: bounded inbox retry, per-UID recovery, no app restart")

if __name__=="__main__":main()
