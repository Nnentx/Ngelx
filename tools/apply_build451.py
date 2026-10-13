from pathlib import Path
p = Path('app/lib/live_broadcast_studio.dart')
s = p.read_text()
start = s.index('class CanliYayinPage')
head, body = s[:start], s[start:]
body = body.replace('backgroundColor: Colors.black,\n        body: Stack', 'backgroundColor: Colors.black,\n        resizeToAvoidBottomInset: false,\n        body: Stack', 1)
body = body.replace('SafeArea(child: Padding(\n            padding: const EdgeInsets.all(14),', 'SafeArea(child: Padding(\n            padding: EdgeInsets.fromLTRB(14,14,14,14+MediaQuery.of(context).viewInsets.bottom),', 1)
body = body.replace('const BoxConstraints(maxWidth:340,maxHeight:220)', 'BoxConstraints(maxWidth:280,maxHeight:MediaQuery.of(context).viewInsets.bottom>0?64:120)', 1)
body = body.replace('padding:const EdgeInsets.all(9)', 'padding:const EdgeInsets.all(5)', 1)
body = body.replace(".limit(30).snapshots()", ".limit(3).snapshots()", 1)
body = body.replace('maxLines:2,', 'maxLines:1,', 1)
body = body.replace("padding:const EdgeInsets.fromLTRB(12,12,12,8)", "padding:const EdgeInsets.all(6)", 1)
body = body.replace("color:Colors.white,borderRadius:BorderRadius.vertical(top:Radius.circular(26))", "color:Color(0xDDFFFFFF),borderRadius:BorderRadius.all(Radius.circular(24))", 1)
body = body.replace('                Ngelx448GuestControls(', '                if(MediaQuery.of(context).viewInsets.bottom==0)Ngelx448GuestControls(', 1)
body = body.replace('                const SizedBox(height:10),\n                if(widget.yayinSahibi)Row', '                if(MediaQuery.of(context).viewInsets.bottom==0)...[\n                const SizedBox(height:6),\n                if(widget.yayinSahibi)Row', 1)
body = body.replace("              ]))),", "                ],\n              ]))),", 1)
# The top close button already confirms ending the broadcast; keep a single exit.
line = next((x for x in body.splitlines() if "if(widget.yayinSahibi)Padding" in x and "label:const Text('Yayını bitir')" in x), None)
if line:
    body = body.replace(line, '')
body = body.replace('controller:yorum,enabled:etkin', 'textInputAction:TextInputAction.send,controller:yorum,enabled:etkin', 1)
body = body.replace('hintText:hint,hintStyle:', 'isDense:true,contentPadding:const EdgeInsets.symmetric(horizontal:12,vertical:10),hintText:hint,hintStyle:', 1)
p.write_text(head+body)
print('Build451 compact live overlay applied')

# Keep discovery category filters consistent with the approved white/purple UI.
p=Path('app/lib/main.dart')
s=p.read_text();start=s.index('class _KesfetPageState');end=s.index('class _TrendEtiketi',start)
section=s[start:end].replace('ChoiceChip(', 'ChoiceChip(selectedColor:const Color(0xFFF0E8FF),backgroundColor:Colors.white,checkmarkColor:mor,labelStyle:const TextStyle(color:mor,fontWeight:FontWeight.w700),')
p.write_text(s[:start]+section+s[end:])
