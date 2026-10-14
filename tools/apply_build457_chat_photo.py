"""Build457 chat-photo UX: distinguish upload from message save and retry renders.

Patch only the generated private chat (not group/community media uploads).
Applied after Build456 and prior Build457 widget transformations.
No duplicate upload retry, no Firestore schema or account modifications.
"""
from pathlib import Path

SOURCE=Path("app/lib/main.dart")

PHOTO_CLASS="class NgelXSohbetFotoOnizleme extends StatelessWidget{"
NEXT_CLASS="class NgelXSohbetVideoOnizleme extends StatelessWidget{"
PRIVATE_METHOD="  Future<void> medyaGonder(ImageSource kaynak) async {"
PRIVATE_END="  Future<void> videoGonder(ImageSource kaynak)async{"
SAVE_ANCHOR="""      ).timeout(const Duration(minutes:2));

      final ref=FirebaseFirestore.instance.collection('chats').doc(widget.chatId);"""
SAVE_REPLACEMENT="""      ).timeout(const Duration(minutes:2));

      // Upload completion does NOT mean the chat message was committed yet.
      _ekIslemBaslat('Fotoğraf mesajı kaydediliyor…');
      final ref=FirebaseFirestore.instance.collection('chats').doc(widget.chatId);"""
RENDER_ANCHOR="          error:hata(),"
RENDER_REPLACEMENT="""          error:hata(),
          retryErrorBuilder: (context,error,retry)=>Container(
            width:230,
            height:180,
            alignment:Alignment.center,
            decoration:BoxDecoration(
              color:const Color(0xFFF3F4F6),
              borderRadius:BorderRadius.circular(16),
            ),
            child:Column(
              mainAxisSize:MainAxisSize.min,
              children:[
                const Icon(Icons.image_not_supported_outlined,color:Color(0xFF6B7280),size:30),
                const SizedBox(height:6),
                const Text('Fotoğraf yüklenemedi',style:TextStyle(color:Color(0xFF4B5563),fontSize:12,fontWeight:FontWeight.w700)),
                const SizedBox(height:6),
                TextButton.icon(
                  onPressed:retry,
                  icon:const Icon(Icons.refresh_rounded,size:18),
                  label:const Text('Tekrar dene'),
                ),
              ],
            ),
          ),"""
WRAP_OLD="IgnorePointer(child:NgelXSohbetFotoOnizleme(url:medyaUrl))"
WRAP_NEW="NgelXSohbetFotoOnizleme(url:medyaUrl)"

def replace_exact(haystack,old,new,context):
    count=haystack.count(old)
    if count!=1:
        raise ValueError(f"Build457 photo {context} source changed: expected one anchor, got {count}")
    return haystack.replace(old,new,1)

def transform(source):
    if "Fotoğraf mesajı kaydediliyor…" in source and "retryErrorBuilder: (context,error,retry)=>Container(" in source:
        return source
    a=source.index(PHOTO_CLASS)
    b=source.index(NEXT_CLASS,a)
    photo=source[a:b]
    photo=replace_exact(photo,RENDER_ANCHOR,RENDER_REPLACEMENT,"preview")
    source=source[:a]+photo+source[b:]
    a=source.index(PRIVATE_METHOD)
    b=source.index(PRIVATE_END,a)
    method=source[a:b]
    method=replace_exact(method,SAVE_ANCHOR,SAVE_REPLACEMENT,"private photo save")
    source=source[:a]+method+source[b:]
    source=replace_exact(source,WRAP_OLD,WRAP_NEW,"photo preview interaction")
    return source

def main():
    before=SOURCE.read_text()
    after=transform(before)
    if after!=before: SOURCE.write_text(after)
    print("Build457: private photo upload -> save stage and retryable preview; no media writes")

if __name__=="__main__":
    main()
