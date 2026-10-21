part of 'main.dart';

// The badge follows the rendered image, including after its size resolves.
class Ngelx551MediaReaction extends StatelessWidget {
  final Widget media, badge;
  const Ngelx551MediaReaction({super.key, required this.media, required this.badge});
  @override Widget build(BuildContext context) => Stack(
    clipBehavior: Clip.none,
    children: [
      Padding(padding: const EdgeInsets.only(bottom:12), child:media),
      Positioned(right:0, bottom:0, child:badge),
    ],
  );
}

class Ngelx551CallGrid extends StatelessWidget {
  final int count, columns;
  final bool voice;
  final IndexedWidgetBuilder itemBuilder;
  const Ngelx551CallGrid({super.key, required this.count, required this.columns,
    required this.voice, required this.itemBuilder});
  @override Widget build(BuildContext context) => LayoutBuilder(builder:(context,c) {
    final compact = voice && count == 2;
    final rows = math.max(1,(count / columns).ceil());
    final tileWidth = math.max(0.0,(c.maxWidth-24-10*(columns-1))/columns);
    final height = compact
      ? math.min(c.maxHeight, math.min(320.0, tileWidth*1.35)+18)
      : c.maxHeight;
    final extent = compact
      ? math.max(1.0,height-18)
      : ((c.maxHeight-18-10*(rows-1))/rows).clamp(130.0,1200.0).toDouble();
    return Center(child:SizedBox(height:height, child:GridView.builder(
      padding:const EdgeInsets.fromLTRB(12,6,12,12),
      itemCount:count,
      gridDelegate:SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount:columns,crossAxisSpacing:10,mainAxisSpacing:10,mainAxisExtent:extent),
      itemBuilder:itemBuilder,
    )));
  });
}
