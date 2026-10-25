# Build570 Ludo artwork, observers and join tone

Uses complete verified Build569 source. Classic and Power share beveled board, real 3D pawn sprites, large dice and 10-second ring. Classic omits power items. Power pickups increment capped inventory; visible red badges show remaining items. Quick message chips use existing server chat and three-second bubbles. Pawns move square-by-square at 160 ms per square (five squares 800 ms), with a small hop.

Authenticated spectators enter through six-digit code and read-only watch action. Presence expires after 25 seconds; explicit leave removes it. Watchers never acquire seats or invoke game mutations. Players see count in the header.

All-home players receive up to three opening rolls. Dice generator remains unbiased; no weighted sixes. Starting rules apply to two and four player games.

Group call join sound is owned by persistent call lifecycle, including minimized calls. Initial roster, departure and reconnect restoration do not chime; new remote identity does. Audio player does not activate or replace audio session. Tone is generated at assembly, quiet two-note 360 ms WAV. Call detach disposes listener and player.

122 Node tests passed before CI. Flutter tests, analyzer, renderer previews and existing APK signer are verified by build workflow. Actual hardware audio routing still needs device listening verification.

Performance follow-up: chat composer has independent state; polling only rebuilds message list while typing; behind-sheet clock and whole-room rebuilds pause; board has a repaint boundary. Compressed image memory cache is capped at 24 MiB; image validity checks decode at width 32 rather than full resolution; 47 simple avatar sites decode at width 384. Original media bytes remain unchanged. Hidden call page does not rebuild each second.
