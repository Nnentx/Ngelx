part of 'main.dart';

/// Presentation only. All controllers, callbacks and live data remain owned by
/// the existing inbox and friends strip.
bool ngelx560ShowProfiles(MediaQueryData media) {
  final available =
      media.size.height - media.viewInsets.bottom - media.padding.vertical;
  final extra = math.max(0, media.textScaler.scale(12) / 12 - 1) * 56;
  return available >= (media.viewInsets.bottom > 0 ? 480 : 360) + extra;
}

double ngelx560ProfileHeight(TextScaler scaler) =>
    124 + math.max(0, scaler.scale(12) / 12 - 1) * 56;

class Ngelx560InboxHeader extends StatelessWidget {
  final String title, searchHint;
  final bool searchOpen;
  final TextEditingController controller;
  final FocusNode focusNode;
  final ValueChanged<String> onChanged;
  final VoidCallback onToggleSearch, onNew;
  const Ngelx560InboxHeader({
    super.key,
    required this.title,
    required this.searchHint,
    required this.searchOpen,
    required this.controller,
    required this.focusNode,
    required this.onChanged,
    required this.onToggleSearch,
    required this.onNew,
  });
  @override
  Widget build(BuildContext context) => Padding(
    padding: const EdgeInsets.fromLTRB(16, 10, 12, 6),
    child: LayoutBuilder(
      builder: (context, box) {
        final searchWidth = math.min(
          164.0,
          math.max(82.0, (box.maxWidth - 60) / 2),
        );
        return SizedBox(
          height: math.max(
            48.0,
            MediaQuery.textScalerOf(context).scale(13) * 1.4 + 24,
          ),
          child: Row(
            children: [
              Expanded(
                child: Align(
                  alignment: Alignment.centerLeft,
                  child: FittedBox(
                    key: const ValueKey('inbox-title-fit560'),
                    fit: BoxFit.scaleDown,
                    alignment: Alignment.centerLeft,
                    child: Text(
                      title,
                      key: const ValueKey('inbox-title560'),
                      maxLines: 1,
                      style: const TextStyle(
                        color: Color(0xFF07142E),
                        fontSize: 26,
                        fontWeight: FontWeight.w800,
                        letterSpacing: -.6,
                      ),
                    ),
                  ),
                ),
              ),
              const SizedBox(width: 6),
              if (searchOpen)
                SizedBox(
                  width: searchWidth,
                  height: math.max(
                    40.0,
                    MediaQuery.textScalerOf(context).scale(13) * 1.4 + 20,
                  ),
                  child: TextField(
                    key: const ValueKey('inbox-search445'),
                    controller: controller,
                    focusNode: focusNode,
                    onChanged: onChanged,
                    textInputAction: TextInputAction.search,
                    onSubmitted: (_) => focusNode.unfocus(),
                    style: const TextStyle(
                      color: Color(0xFF111827),
                      fontSize: 13,
                    ),
                    decoration: InputDecoration(
                      hintText: searchHint,
                      hintStyle: const TextStyle(
                        color: Color(0xFF8C879D),
                        fontSize: 10.5,
                      ),
                      isDense: true,
                      contentPadding: const EdgeInsets.only(
                        left: 10,
                        top: 10,
                        bottom: 10,
                      ),
                      suffixIconConstraints: const BoxConstraints(
                        minWidth: 32,
                        maxWidth: 36,
                        minHeight: 40,
                      ),
                      suffixIcon: IconButton(
                        key: const ValueKey('inbox-search-close560'),
                        tooltip: 'Aramayı kapat',
                        padding: EdgeInsets.zero,
                        onPressed: onToggleSearch,
                        icon: const Icon(
                          Icons.close_rounded,
                          color: Color(0xFF8C879D),
                          size: 18,
                        ),
                      ),
                      filled: true,
                      fillColor: const Color(0xFFF3F0F9),
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(20),
                        borderSide: BorderSide.none,
                      ),
                    ),
                  ),
                )
              else
                IconButton(
                  key: const ValueKey('inbox-search-open560'),
                  tooltip: searchHint,
                  onPressed: onToggleSearch,
                  icon: const Icon(Icons.search_rounded, color: mor, size: 24),
                ),
              const SizedBox(width: 4),
              IconButton(
                key: const ValueKey('inbox-new560'),
                tooltip: 'Yeni sohbet',
                onPressed: onNew,
                icon: const Icon(
                  Icons.add_circle_rounded,
                  color: mor,
                  size: 32,
                ),
              ),
            ],
          ),
        );
      },
    ),
  );
}

class Ngelx560CategoryRow extends StatelessWidget {
  final List<Widget> children;
  const Ngelx560CategoryRow({super.key, required this.children});
  @override
  Widget build(BuildContext context) => LayoutBuilder(
    builder: (context, box) {
      final width = math.max(68.0, box.maxWidth / math.max(1, children.length));
      return SizedBox(
        height: 48,
        child: SingleChildScrollView(
          scrollDirection: Axis.horizontal,
          child: Row(
            children: [
              for (final tab in children) SizedBox(width: width, child: tab),
            ],
          ),
        ),
      );
    },
  );
}

class Ngelx560ProfileRail extends StatelessWidget {
  final String uid;
  final int itemCount;
  final IndexedWidgetBuilder itemBuilder;
  const Ngelx560ProfileRail({
    super.key,
    required this.uid,
    required this.itemCount,
    required this.itemBuilder,
  });
  @override
  Widget build(BuildContext context) => SizedBox(
    height: ngelx560ProfileHeight(MediaQuery.textScalerOf(context)),
    child: ListView.builder(
      key: PageStorageKey('inbox-friends-' + uid),
      scrollDirection: Axis.horizontal,
      padding: const EdgeInsets.fromLTRB(12, 2, 12, 4),
      itemExtent: 90,
      itemCount: itemCount,
      itemBuilder: itemBuilder,
    ),
  );
}

class Ngelx560CategoryChip extends StatelessWidget {
  final String label, countLabel;
  final bool selected, showCount;
  final VoidCallback onTap;
  const Ngelx560CategoryChip({
    super.key,
    required this.label,
    required this.countLabel,
    required this.selected,
    required this.showCount,
    required this.onTap,
  });
  @override
  Widget build(BuildContext context) => Padding(
    padding: const EdgeInsets.symmetric(horizontal: 2),
    child: InkWell(
      borderRadius: BorderRadius.circular(20),
      onTap: onTap,
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 180),
        padding: const EdgeInsets.symmetric(horizontal: 4, vertical: 9),
        decoration: BoxDecoration(
          gradient: selected
              ? const LinearGradient(
                  colors: [
                    Color(0xFF13C8EE),
                    Color(0xFF176EF4),
                    Color(0xFF6E45F5),
                  ],
                )
              : null,
          color: selected ? null : const Color(0xFFF5F7FB),
          borderRadius: BorderRadius.circular(20),
          boxShadow: selected
              ? const [
                  BoxShadow(
                    color: Color(0x263B82F6),
                    blurRadius: 14,
                    offset: Offset(0, 5),
                  ),
                ]
              : null,
        ),
        child: Stack(
          clipBehavior: Clip.none,
          children: [
            FittedBox(
              fit: BoxFit.scaleDown,
              child: Text(
                label,
                maxLines: 1,
                style: TextStyle(
                  color: selected ? Colors.white : const Color(0xFF6F7891),
                  fontSize: 12.5,
                  fontWeight: selected ? FontWeight.w900 : FontWeight.w700,
                ),
              ),
            ),
            if (showCount)
              Positioned(
                right: -3,
                top: -8,
                child: Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 4,
                    vertical: 1,
                  ),
                  decoration: BoxDecoration(
                    color: const Color(0xFFE62D48),
                    borderRadius: BorderRadius.circular(20),
                  ),
                  child: Text(
                    countLabel,
                    style: const TextStyle(
                      color: Colors.white,
                      fontSize: 9,
                      fontWeight: FontWeight.w900,
                    ),
                  ),
                ),
              ),
          ],
        ),
      ),
    ),
  );
}
