import 'dart:math' as math;
import 'package:flutter/material.dart';

/// Presentation only: the caller retains ownership of the composer and RTC.
class Ngelx540LiveBar extends StatelessWidget {
  final Widget composer;
  final List<Widget> actions;
  const Ngelx540LiveBar({super.key, required this.composer, required this.actions});
  @override
  Widget build(BuildContext context) => Material(
    color: Colors.transparent,
    borderRadius: BorderRadius.circular(24),
    child: Padding(
      padding: const EdgeInsets.symmetric(horizontal: 4, vertical: 2),
      child: Row(children: [
        Expanded(child: composer),
        if (MediaQuery.viewInsetsOf(context).bottom == 0) ...actions,
      ]),
    ),
  );
}

class Ngelx540LiveAction extends StatelessWidget {
  final Widget icon;
  final String label;
  final VoidCallback? onPressed;
  const Ngelx540LiveAction({super.key, required this.icon,
    required this.label, required this.onPressed});
  @override
  Widget build(BuildContext context) => SizedBox(width: 44, child: Tooltip(
    message: label, child: InkWell(onTap: onPressed,
      borderRadius: BorderRadius.circular(22),
      child: Padding(padding: const EdgeInsets.symmetric(vertical: 4),
        child: Column(mainAxisSize: MainAxisSize.min, children: [
          SizedBox(height: 32, child: Center(child: icon)),
          SizedBox(height: 18, child: FittedBox(fit: BoxFit.scaleDown,
            child: Text(label, style: const TextStyle(color: Colors.white, fontSize: 10)))),
        ])),
    ),
  ));
}

/// Keep the mini call above the keyboard and inside the usable viewport.
Offset ngelx540BoundMini(Offset point, Size screen, EdgeInsets padding,
    double keyboard, double width) {
  final left = math.min(8.0, math.max(0.0, screen.width - width));
  final right = math.max(left, screen.width - width - 8);
  final top = math.min(padding.top + 8, math.max(0.0, screen.height - 220));
  final bottom = math.max(top,
      screen.height - math.max(padding.bottom, keyboard) - 220);
  return Offset(point.dx.clamp(left, right).toDouble(),
      point.dy.clamp(top, bottom).toDouble());
}

Offset ngelx540SnapMini(Offset point, Size screen, EdgeInsets padding,
    double keyboard, double width) => ngelx540BoundMini(
  Offset(point.dx + width / 2 < screen.width / 2 ? 8 : screen.width - width - 8,
      point.dy), screen, padding, keyboard, width);
