# Build585 feedback implementation

Base: c999d229d68ea9d79911d2e9821a711814d17455 and the exact Build584 assembled source from successful Actions run 40757681279 (artifact 12847118094).

The assembly patch leaves settings, board layout, player cards, chat, rewards and the existing server game rules intact. Pawn movement changes from 190ms to 110ms per step (six steps: 1140ms to 660ms), with step audio following the same pace. A single legal move runs after a 220ms pause, while multiple choices wait for the player. Spectator, app lifecycle, turn, revision, leave and Auto guards are retained. Remove only the extra footer die/GO, countdown, two quick-message buttons and redundant last-die caption. The player-avatar die remains usable.

Call registration now uses a stable SHA-256 token document ID in both native token refresh and foreground registration. Native onNewToken refreshes the signed-in user's registration. The push relay reads past duplicate documents before selecting two distinct devices, and the caller retries when every attempted registration was rejected and pruned. Existing authentication, block and notification preferences remain enforced.

Validation completed locally: 184 Node tests passed across game engine, live moderation and call push; assembly patch applied successfully and a second application was idempotent; Python syntax and git diff whitespace checks passed.

Pending: Flutter analysis/widget suite, Android compilation and signature verification, two-phone background/locked-screen calling in both directions. The local environment has no Flutter SDK; exact SDK download was unavailable. The dedicated review workflow is prepared but has not run. No updated APK was created, no production worker was deployed and no in-app updater was changed.

The user explicitly approved sending this implementation to the Nnentx/Ngelx repository and building the review APK. The change is prepared on a separate review branch; it does not deploy production services or modify the in-app updater.
