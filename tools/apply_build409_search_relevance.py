#!/usr/bin/env python3
"""NgelX Build 409 — restore usable search results without profile redesign.
Applies to the generated Build 408 main.dart, after all previous patch scripts.
"""
from pathlib import Path
p=Path("app/lib/main.dart")
m=p.read_text(encoding="utf-8")
start=m.index("class _AramaPageState extends State<AramaPage>")
end=m.index("\nclass HikayeSeridi",start)
s=m[start:end]
old="""                 final icerikler = snap.data![1].docs.where((d){"""
new="""                 final adayIcerikler = snap.data![1].docs.where((d){"""
if s.count(old)!=1:raise SystemExit("Search content source anchor drifted")
s=s.replace(old,new,1)
needle="""                   return puan(b.data()).compareTo(puan(a.data()));
                 });
                 if (kullanicilar.isEmpty && icerikler.isEmpty)"""
replace="""                   final karsilastir=puan(b.data()).compareTo(puan(a.data()));
                   if(karsilastir!=0)return karsilastir;
                   final at=a.data()['createdAt'],bt=b.data()['createdAt'];
                   final aMs=at is Timestamp?at.millisecondsSinceEpoch:0;
                   final bMs=bt is Timestamp?bt.millisecondsSinceEpoch:0;
                   return bMs.compareTo(aMs);
                 });
                 // Identical media copied into several post documents should only
                 // occupy one search result. Match canonical media IDs/URLs, never
                 // assume two different videos are identical because their titles match.
                 final gorulenMedya=<String>{};
                 final icerikler=adayIcerikler.where((d){
                   final v=d.data();
                   final sabitId=(v['sourceVideoId']??v['contentHash']??'').toString().trim();
                   if(sabitId.isNotEmpty)return gorulenMedya.add('id:'+sabitId);
                   final ham=(v['mediaUrl']??v['videoUrl']??v['originalUrl']??'').toString().trim();
                   if(ham.isEmpty)return gorulenMedya.add('post:'+d.id);
                   final url=Uri.tryParse(ham);
                   final medya=url==null?ham:url.replace(query:'',fragment:'').toString();
                   return gorulenMedya.add('media:'+medya);
                 }).toList();
                 if (kullanicilar.isEmpty && icerikler.isEmpty)"""
if s.count(needle)!=1:raise SystemExit("Search post-ranking anchor drifted")
s=s.replace(needle,replace,1)
m=m[:start]+s+m[end:]
p.write_text(m,encoding="utf-8")
print("Build 409 search result ranking and exact-media de-duplication applied.")
