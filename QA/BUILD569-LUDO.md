# Build569 Ludo reference update

Preserves assembled Build568 application and Android signer. Widens board margins; increases board/home contrast; accelerates pawn animation to 120–420 ms; polls authoritative game state each second; shows incoming table messages for three seconds. Inbox create sheet scrolls safely above system navigation. Invite list has explicit bottom clearance.

Authoritative turn and move windows are ten seconds. Expiry rolls or selects the first legal pawn through normal engine actions, preserving captures, safe cells, exact finish and bonus turns. Every roll resets the move window. New rooms use numeric six-digit IDs; existing legacy links remain readable. Deploy prepared bot/match service after APK validation.

Validation: 45 Node tests pass locally, including timeout captures, delayed rolls and stale-action rejection. Flutter tests, analysis, APK signature and preserved assets are checked in CI. Release publication follows verified build.
