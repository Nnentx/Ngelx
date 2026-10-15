#!/usr/bin/env python3
"""Build461: repair actual cover mode flow and cover loading, not cosmetic fake states.

Apply strictly AFTER the Build460 transforms have generated app/lib/main.dart.
No production Firebase/R2 changes, user-data deletion or media migration.
"""
from pathlib import Path
MAIN = Path("app/lib/main.dart")


def single(s, before, after, label):
    count=s.count(before)
    if count!=1:
        raise ValueError(f"Build461 {label}: expected exactly 1 location, got {count}")
    return s.replace(before,after,1)


def patch(s):
    if "// Build461 owner mode not inferred from image URL" in s:
        return s

    old="""bool ngelx459KapaksizGorunum(String profilGorunumu,String kapakUrl) =>
  profilGorunumu=='coverless'||kapakUrl.isEmpty;"""
    new="""// Build461 owner mode not inferred from image URL: empty or delayed media must
// not silently override a user's stored 'cover' mode.
bool ngelx459KapaksizGorunum(String profilGorunumu,String kapakUrl) =>
  profilGorunumu!='cover';

String ngelx461BaslangicProfilGorunumu(String? profilGorunumu) =>
  profilGorunumu=='cover'?'cover':'coverless';"""
    s=single(s,old,new,"render choice")

    a=s.index("class _NgelXOnayliProfilDuzenlePageState")
    b=s.index("\nclass ProfilPage extends StatefulWidget",a)
    editor=s[a:b]
    editor=single(editor,
      "_gorunum=widget.ilkGorunum=='coverless'||widget.ilkKapakUrl.isEmpty?'coverless':'cover';",
      "_gorunum=ngelx461BaslangicProfilGorunumu(widget.ilkGorunum);",
      "editor choice should not depend on coverURL")

    # The previous Build460 form validator blocked changing the mode when the
    # stored cover URL was blank. A covered layout can safely display the empty
    # purple placeholder while the user decides whether to upload a cover.
    invalid="""    if(_gorunum=='cover'&&kapak.isEmpty){
      _hata('Kapaklı görünüm için önce bir kapak fotoğrafı ekle.',kapakUyarisi:true);
      return;
    }
"""
    editor=single(editor,invalid,"","cover mode without image")

    # Previously the cover branch had a purple spinner in frameBuilder while
    # the actual remote image was pending. The provider timeout alone does not
    # replace that UI. Use the existing NgelXAgResmi widget with finite error
    # and a real user-controlled retry.
    start=editor.index("child:cover.isNotEmpty?Image(")
    tail="const ColoredBox(color:Color(0xFFF1EAFE),child:Center(child:Icon(Icons.landscape_rounded"
    end=editor.index(tail,start)
    existing=editor[start:end]
    if "frameBuilder" not in existing or "CircularProgressIndicator" not in existing or "errorBuilder" not in existing:
        raise ValueError("Build461 unknown cover image render: refusing broad replacement")
    replacement="""child:cover.isNotEmpty?NgelXAgResmi(
                    url:cover,fit:BoxFit.cover,
                    placeholder:const ColoredBox(color:Color(0xFFF1EAFE),
                      child:Center(child:Icon(Icons.image_outlined,
                        color:Color(0xFF9B87C8),size:36))),
                    retryErrorBuilder:(ctx,error,retry)=>InkWell(
                      onTap:retry,
                      child:const ColoredBox(color:Color(0xFFF1EAFE),
                        child:Center(child:Column(mainAxisSize:MainAxisSize.min,children:[
                          Icon(Icons.refresh_rounded,color:Color(0xFF7C3AED),size:30),
                          SizedBox(height:4),
                          Text('Kapak açılamadı - tekrar dene',
                            style:TextStyle(fontSize:12,color:Color(0xFF7C3AED))),
                        ])))),
                  ):
                    """
    editor=editor[:start]+replacement+editor[end:]

    # A generic 'check your internet' message masked a permission error that
    # would require backend policy changes. Only report safe category strings:
    # never log tokens, usernames, bucket object keys or signed URLs.
    oldcatch="""    }catch(_){
      _hata('Profil kaydedilemedi. Bağlantını kontrol edip tekrar dene.');
    }finally{"""
    newcatch="""    }on FirebaseException catch(e){
      if(e.code=='permission-denied'){
        _hata('Profil izni reddedildi (permission-denied).');
      }else if(e.code=='unauthenticated'){
        _hata('Oturum süresi doldu. Yeniden giriş yap.');
      }else if(e.code=='unavailable'||e.code=='deadline-exceeded'){
        _hata('Bağlantı zaman aşımına uğradı. Yeniden dene.');
      }else{
        _hata('Profil kaydedilemedi. Hata kodu: '+e.code);
      }
    }catch(_){
      _hata('Profil kaydedilemedi. Yeniden dene.');
    }finally{"""
    editor=single(editor,oldcatch,newcatch,"safe persistence error categories")
    s=s[:a]+editor+s[b:]
    return s


def main():
    source=MAIN.read_text(encoding="utf-8")
    result=patch(source)
    if result!=source:MAIN.write_text(result,encoding="utf-8")
    print("Build461: cover mode/save no longer depends on URL; cover loader has finite retry; safe save errors distinguished.")


if __name__=="__main__":
    main()
