#!/usr/bin/env python3
"""Build 416: make profile-post search distinguish people search.

No changes to search permissions, existing post filters, profile UI, or
Firestore writes; reuse the global user search with the current query.
"""
from pathlib import Path

p=Path('app/lib/main.dart')
s=p.read_text(encoding='utf-8')
a=s.index('class _ProfilAramaPageState extends State<ProfilAramaPage>')
b=s.index('\nclass ',a+12)
profile=s[a:b]

def one(old,new,label):
    global profile
    n=profile.count(old)
    if n!=1:
        raise SystemExit(f'Build 416 {label}: expected one marker, got {n}')
    profile=profile.replace(old,new,1)

one("hintText:'Profilde anahtar kelime ara'",
    "hintText:'Paylaşım ara veya Kişiler seç'",
    "search scope hint")
one("""              onSelected:(_)=>setState(()=>tur=kod),""",
"""              onSelected:(_){
                if(kod=='people'){
                  Navigator.push(context,MaterialPageRoute(
                    builder:(_)=>AramaPage(baslangicSorgu:q)));
                }else{
                  setState(()=>tur=kod);
                }
              },""",
    "people chip routes to global account search")
one("""                  chip('all','Tümü',Icons.grid_view_rounded),
                  chip('photo','Fotoğraf',Icons.photo_outlined),""",
"""                  chip('all','Tümü',Icons.grid_view_rounded),
                  chip('people','Kişiler',Icons.people_alt_outlined),
                  chip('photo','Fotoğraf',Icons.photo_outlined),""",
    "make people visible after all")
one("""                    Text(q.isEmpty?'Bu kategoride paylaşım yok.':'Eşleşen paylaşım bulunamadı.',style:const TextStyle(color:Colors.black54,fontWeight:FontWeight.w700)),
                  ]))""",
"""                    Text(q.isEmpty?'Bu kategoride paylaşım yok.':'Eşleşen paylaşım bulunamadı.',
                      textAlign:TextAlign.center,
                      style:const TextStyle(color:Colors.black54,fontWeight:FontWeight.w700)),
                    if(q.isNotEmpty)...[
                      const SizedBox(height:12),
                      TextButton.icon(
                        icon:const Icon(Icons.people_alt_outlined),
                        label:const Text('Kişilerde ara'),
                        onPressed:()=>Navigator.push(context,
                          MaterialPageRoute(builder:(_)=>AramaPage(baslangicSorgu:q))),
                      ),
                    ],
                  ]))""",
    "no-post results provide useful path to people")
s=s[:a]+profile+s[b:]
p.write_text(s,encoding='utf-8')
print('Build 416 profile post search now visibly links to safe global people search.')
