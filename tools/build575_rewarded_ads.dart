part of 'main.dart';

// This optional component is assembled ONLY with the publisher's AdMob IDs.
// Client ad callbacks never mutate coins. The server-side verified callback does.
class Ngelx575RewardedVideo {
 static const adUnit=String.fromEnvironment('NGELX_ADMOB_REWARDED_UNIT',defaultValue:'');
 final Future<Map<String,dynamic>> Function(Map<String,dynamic>) request;
 const Ngelx575RewardedVideo(this.request);

 Future<String> watch() async {
  if(adUnit.isEmpty)return 'Video ödülü henüz etkin değil.';
  // Tokens are short lived, owned by the authenticated NgelX user.
  late final String token;
  try{
   final session=await request({'action':'ad_session'});
   token=(session['token']??'').toString();
   if(!RegExp(r'^[a-f0-9]{32}$').hasMatch(token))return 'Video ödülü şu anda kullanılamıyor.';
  }catch(_){return 'Video ödülü sunucuda henüz etkin değil.';}
  try{
   await MobileAds.instance.initialize().timeout(const Duration(seconds:35));
   final completer=Completer<RewardedAd?>();
   RewardedAd.load(
    adUnitId:adUnit,
    request:const AdRequest(),
    rewardedAdLoadCallback:RewardedAdLoadCallback(
     onAdLoaded:(ad){if(!completer.isCompleted)completer.complete(ad);else ad.dispose();},
     onAdFailedToLoad:(error){if(!completer.isCompleted)completer.complete(null);},
    ),
   );
   final ad=await completer.future.timeout(const Duration(seconds:25),onTimeout:()=>null);
   if(ad==null)return 'Şu anda gösterilebilecek video yok.';
   // Google signs this custom_data in its own SSV callback.
   await ad.setServerSideOptions(ServerSideVerificationOptions(customData:token));
   final dismissed=Completer<bool>();var earned=false;
   ad.fullScreenContentCallback=FullScreenContentCallback<RewardedAd>(
    onAdDismissedFullScreenContent:(ad){
     ad.dispose();
     if(!dismissed.isCompleted)dismissed.complete(earned);
    },
    onAdFailedToShowFullScreenContent:(ad,error){
     ad.dispose();
     if(!dismissed.isCompleted)dismissed.complete(false);
    },
   );
   await ad.show(onUserEarnedReward:(ad,reward){earned=true;});
   final watched=await dismissed.future.timeout(const Duration(minutes:3),onTimeout:()=>false);
   if(!watched)return 'Video tamamlanmadı; çip verilmedi.';
   // This polls read-only status. It never sends a client-controlled credit amount.
   for(var tries=0;tries<9;tries++){
    try{
     final result=await request({'action':'ad_status','token':token});
     if(result['verified']==true)return '+30 çip hesabına eklendi! 🎁';
    }catch(_){/* Google SSV or mobile connectivity may be delayed. */}
    await Future<void>.delayed(const Duration(seconds:2));
   }
   return 'Video izlendi. Çip ödülün sunucuda doğrulanınca hesabında görünecek.';
  }catch(_){return 'Video açılamadı. Onaylanmamış bir ödül verilmedi.';}
 }
}
