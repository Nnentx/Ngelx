"""Apply narrow avatar HTTP performance fixes after full Build457 generation.

Build456 already deduplicates requests and enforces a byte-size budget.
Do not reintroduce another download cache. This patch only reuses the Dio
transport and permits standard HTTP caching; private 401/403 retries keep
their existing authenticated behavior. Fail closed on unknown source shape.
"""
from pathlib import Path

FILE=Path("app/lib/main.dart")
CLIENT="""final Dio _ngelx457AvatarHttp = Dio(BaseOptions(
  connectTimeout:const Duration(seconds:12),
  receiveTimeout:const Duration(seconds:45),
  validateStatus:(s)=>s!=null,
));
"""
OLD_TRANSPORT="""    return Dio(BaseOptions(
      connectTimeout:const Duration(seconds:12),
      receiveTimeout:const Duration(seconds:45),
      validateStatus:(s)=>s!=null,
    )).getUri<List<int>>("""
NEW_TRANSPORT="""    return _ngelx457AvatarHttp.getUri<List<int>>("""
NO_CACHE="""          'Cache-Control':'no-cache, no-store, max-age=0',
          'Pragma':'no-cache',
"""
START="Future<Uint8List> _ngelxAgResmiBaytlari456(String rawUrl) async {"
END="@immutable\nclass NgelXAgImageProvider"
ANCHOR="final _ngelx456ImageRequests=<String,Future<Uint8List>>{};"

def transform(source:str)->str:
    if "_ngelx457AvatarHttp.getUri<List<int>>(" in source:
        return source
    assert source.count(START)==1 and source.count(END)==1
    assert source.count(ANCHOR)==1, "Requires Build456 shared request cache"
    left=source.index(START)
    right=source.index(END,left)
    section=source[left:right]
    assert section.count(OLD_TRANSPORT)==1, "Avatar transport has changed"
    assert section.count(NO_CACHE)==1, "Unexpected request cache headers"
    section=section.replace(OLD_TRANSPORT,NEW_TRANSPORT,1)
    section=section.replace(NO_CACHE,"",1)
    source=source[:left]+section+source[right:]
    source=source.replace(ANCHOR,ANCHOR+"\n"+CLIENT,1)
    assert source.count("_ngelx457AvatarHttp.getUri<List<int>>(")==1
    assert "_ngelx456ImageRequests.putIfAbsent(" in source
    return source

def main()->None:
    src=FILE.read_text(encoding="utf-8")
    after=transform(src)
    if after!=src:FILE.write_text(after,encoding="utf-8")
    print("Build457: reused avatar HTTP connection; retained Build456 dedup/cache budget.")

if __name__=="__main__":
    main()
