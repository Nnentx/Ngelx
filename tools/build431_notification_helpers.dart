bool ngelxBildirimKaydiGecerli(String collection, Map<String,dynamic> v, String uid) {
  return collection=='notifications' && v['toUid']==uid &&
    (v['type']!=null || v['eventKind']!=null ||
      ['text','message','content'].any((k)=>(v[k]??'').toString().trim().isNotEmpty));
}

String ngelxBildirimMetni(Map<String,dynamic> v) {
  var text='';
  for(final key in ['text','message','content']) {
    final value=(v[key]??'').toString().trim();
    if(value.isNotEmpty){text=value;break;}
  }
  final name=(v['senderName']??v['fromName']??'').toString().trim();
  if(text.isEmpty){
    final kind=(v['type']??v['eventKind']??'').toString();
    text=switch(kind){
      'follow_request'=>'seni takip etmek istiyor',
      'friend_request'=>'sana arkadaşlık isteği gönderdi',
      'follow_accepted'=>'takip isteğini kabul etti',
      'friend_accepted'=>'arkadaşlık isteğini kabul etti',
      'like'=>'gönderini beğendi',
      'comment'=>'gönderine yorum yaptı',
      'live'=>'canlı yayın başlattı',
      'security'=>'Hesap güvenliği bildirimi',
      _=>'Bildirim ayrıntısı bulunamadı',
    };
  }
  return name.isEmpty||text.toLowerCase().startsWith(name.toLowerCase())?text:'$name $text';
}

dynamic ngelxBildirimTarihi(Map<String,dynamic> v) {
  for(final key in ['createdAt','clientCreatedAt','timestamp']){
    final value=v[key];
    if(value is Timestamp)return value;
    if(value is DateTime)return Timestamp.fromDate(value);
    if(value is String){final date=DateTime.tryParse(value);if(date!=null)return Timestamp.fromDate(date);}
  }
  return null;
}

bool ngelxBekleyenMesajIstegi(Map<String,dynamic> v,String uid,Set<String> friends){
  final members=v['members'] is Iterable?(v['members'] as Iterable).map((e)=>e.toString()).toList():<String>[];
  if(v['isGroup']==true||members.length!=2||!members.contains(uid))return false;
  final other=members.firstWhere((x)=>x!=uid,orElse:()=>uid);
  return other!=uid && !friends.contains(other) &&
    (v['lastMessage']??'').toString().trim().isNotEmpty &&
    v['requestRecipientUid']==uid && v['requestAccepted_$uid']!=true &&
    v['requestRejected_$uid']!=true &&
    !(v['hiddenFor'] is Iterable && (v['hiddenFor'] as Iterable).contains(uid));
}
