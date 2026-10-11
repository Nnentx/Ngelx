"""Keep durable delete queue and prevent success feedback for concurrent no-ops."""
from pathlib import Path
p=Path('app/lib/main.dart');s=p.read_text()
if '// Build438 deletion outcome' not in s:
    start=s.index('Future<void> ngelx435MesajiSil(');end=s.index('Future<void> ngelx435SilmeTekrar(',start)
    part=s[start:end]
    old='  if(!_ngelx435SilmeKilidi.add(lock))return;'
    assert part.count(old)==1
    part=part.replace(old,"""  // Build438 deletion outcome: an in-flight operation is not a confirmed delete.
  if(!_ngelx435SilmeKilidi.add(lock)){
    if(retry)return;
    throw StateError('Bu mesajın silme işlemi sürüyor. Sonucu bekle.');
  }""")
    part=part.replace('if(FirebaseAuth.instance.currentUser?.uid!=me)return;',"if(FirebaseAuth.instance.currentUser?.uid!=me)throw StateError('Hesap değişti. Silme işlemini kendi hesabından tekrar dene.');")
    s=s[:start]+part+s[end:]
    old="          if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Mesaj silindi.')));"
    assert s.count(old)==2
    s=s.replace(old,"          if(mounted)ngelxDurumMesaji(context,'Mesaj silindi.',tip:'basari');")
    old='          if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text(ngelx436Error(e))));'
    assert s.count(old)==2
    s=s.replace(old,"""          if(mounted)ngelxDurumMesaji(context,
            e is FirebaseException&&e.code=='resource-exhausted'
              ?'Sunucu işlem sınırına ulaştı. Bekleyen silme talebin bu cihazda saklandı. Daha sonra sohbeti tekrar aç.'
              :ngelx436Error(e),
            tip:e is FirebaseException&&e.code=='resource-exhausted'?'uyari':'hata');""")
    p.write_text(s)
