#!/usr/bin/env python3
"""Build 427: keep story follow button in the header, not over the media."""
from pathlib import Path
def one(s,a,b,name):
 n=s.count(a)
 if n!=1:raise SystemExit(f'{name}: expected 1 occurrence, found {n}')
 return s.replace(a,b,1)
p=Path('app/lib/story_v66.dart');s=p.read_text(encoding='utf-8')
s=one(s,
"""                IconButton(onPressed:()=>Navigator.pop(context),icon:const Icon(Icons.close_rounded,color:Colors.white,size:32)),
              ]),
              Row(mainAxisAlignment:MainAxisAlignment.end,children:[
                _takipButonu(),
                if(videoMu)IconButton(onPressed:_sesDegistir,icon:Icon(sessiz?Icons.volume_off_rounded:Icons.volume_up_rounded,color:Colors.white,size:28)),
                IconButton(onPressed:_secenekler,icon:const Icon(Icons.more_horiz_rounded,color:Colors.white,size:28)),
              ]),""",
"""                // Follow action belongs to the same compact top header,
                // never to a second row that covers the photo/video.
                _takipButonu(),
                IconButton(onPressed:()=>Navigator.pop(context),icon:const Icon(Icons.close_rounded,color:Colors.white,size:32)),
              ]),
              Row(mainAxisAlignment:MainAxisAlignment.end,children:[
                if(videoMu)IconButton(onPressed:_sesDegistir,icon:Icon(sessiz?Icons.volume_off_rounded:Icons.volume_up_rounded,color:Colors.white,size:28)),
                IconButton(onPressed:_secenekler,icon:const Icon(Icons.more_horiz_rounded,color:Colors.white,size:28)),
              ]),""",'story follow position')
p.write_text(s,encoding='utf-8')
p=Path('app/lib/main.dart');s=p.read_text(encoding='utf-8')
s=one(s,"defaultValue: '426'","defaultValue: '427'",'build number')
s=one(s,"defaultValue: '1.0.201'","defaultValue: '1.0.202'",'build name')
p.write_text(s,encoding='utf-8')
p=Path('app/pubspec.yaml');s=p.read_text(encoding='utf-8')
s=one(s,'version: 1.0.201+426','version: 1.0.202+427','pubspec')
p.write_text(s,encoding='utf-8')
print('Build 427 story follow header layout applied')
