# NgelX Ludo — Build 573 visual acceptance contract

Reference: user-approved large 4-color game board with water/foliage background, compact top gem/coin bar, four player avatars, top-level badge, a compact timer/die and small Power controls.

## Implemented in 573
- Larger portrait board using 0.78-height aspect frame with minimal horizontal padding.
- Position/size calculation fits active pawns inside one 15×15 grid cell; 2–4 pawns sharing a square appear grouped side by side instead of covering each other.
- Existing glossy Ludo pawn atlas retained. Avatar labels shrink and show levels only if supplied by the server.
- Compact timer, die, emoji/chat, quick replies and Power controls below the board.
- Atmospheric water/foliage background rendered in Flutter, so no flattened screenshot is used as fake gameplay UI.
- A truthful wallet UI reads gems/chips from real room fields; when missing, shows a dash instead of invented numbers.
- Existing classic/power modes, room codes, spectators, invitations, live play, fair dice and Power mechanics retained.

## Still outstanding — do not claim done
- The approved static reference image cannot be pixel-identical until bespoke scene artwork and player imagery are available as assets; current 573 uses vector scenery and the existing glossy pawn sprites.
- Wire a server-authoritative chip/diamond/XP/level account ledger and idempotent rewards to the wallet bar; don't grant balances on the client.
- Automatic pawn movement when *exactly one* legal pawn can move; require tap when 2+ legal choices.
- Real-device visual regression/screenshots at 320px, 360px, 393px and 440px Android widths; ensure no game tiles/pawns clip and bottom controls fit.
- Device gameplay confirmation for GO/dice, powers, shield pickup relocation and spectator/voice scenarios.

## Release gate
Only publish to android-update.json after signed APK, automated tests and real-phone gameplay verification. The previously verified Build 572 stays as live in-app update until then.
