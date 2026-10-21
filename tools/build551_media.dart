import 'dart:math' as math;
import 'dart:typed_data';
import 'package:image/image.dart' as img;

bool ngelx551ChatPhotoKind(String kind) =>
  const {'groups','chats','chat-images'}.contains(kind);

// Runs in the existing upload isolate. Keep readable caps at 1600px while
// avoiding a second local decode of the freshly encoded JPEG.
Uint8List ngelx551ChatJpeg(Uint8List bytes) {
  img.Image? original;
  try{original=img.decodeImage(bytes);}
  catch(_){throw const FormatException('Fotoğraf çözülemedi.');}
  if(original==null||original.width<=0||original.height<=0) {
    throw const FormatException('Fotoğraf çözülemedi.');
  }
  var image=img.bakeOrientation(original);
  if(math.max(image.width,image.height)>1600) {
    image=image.width>=image.height
      ?img.copyResize(image,width:1600,interpolation:img.Interpolation.linear)
      :img.copyResize(image,height:1600,interpolation:img.Interpolation.linear);
  }
  return Uint8List.fromList(img.encodeJpg(image,quality:85));
}
