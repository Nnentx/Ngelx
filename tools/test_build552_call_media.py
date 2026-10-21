from pathlib import Path
import tempfile,shutil,sys
from apply_build552_call_media import apply
# Exercise the real generated source; preserve ownership/privacy/mute boundaries.
root=Path(sys.argv[1]) if len(sys.argv)>1 else Path('app/lib')
with tempfile.TemporaryDirectory() as d:
 target=Path(d)/'lib';shutil.copytree(root,target)
 apply(target)
 before={p.name:p.read_bytes() for p in target.glob('*.dart')}
 apply(target)
 assert before=={p.name:p.read_bytes() for p in target.glob('*.dart')},'Transform must be idempotent'
 s=(target/'main.dart').read_text()
 start=s.index('class NgelXGorulenBildirim');end=s.index('bool ngelxBildirimKaydiGecerli',start)
 assert '.update(' not in s[start:end] and 'Timer' not in s[start:end]
 assert "'readAt':FieldValue.serverTimestamp()" in s,'Explicit read action must remain'
 assert '_owns444=ngelxCallSession444.attach(widget.roomName)' in s
 lifecycle=(target/'build446_call_lifecycle.dart').read_text()
 assert 'if(state==AppLifecycleState.inactive)return;' in lifecycle
 assert 'stopCameraCaptureOnMute:true' in lifecycle
 assert '!entry.muted' in lifecycle
 photo=(target/'build548_widgets.dart').read_text()
 assert 'generation!=_generation' in photo and 'Yeniden dene' in photo
 assert 'ngelxAgResmiOnbelleginiTemizle(url)' in photo
 print('Build552 generated source, privacy boundaries, explicit reads and idempotency passed')
