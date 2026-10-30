# Build585 feedback implementation

Base: c999d229d68ea9d79911d2e9821a711814d17455 and the exact Build584 assembled source from successful Actions run 40757681279 (artifact 12847118094).

The assembly patch leaves settings, board layout, player cards, chat, rewards and the existing server game rules intact. Pawn movement changes from 190ms to 110ms per step (six steps: 1140ms to 660ms), with step audio following the same pace. A single legal move runs after a 220ms pause, while multiple choices wait for the player. Spectator, app lifecycle, turn, revision, leave and Auto guards are retained. Remove only the extra footer die/GO, countdown, two quick-message buttons and redundant last-die caption. The player-avatar die remains usable.

Call registration now uses a stable SHA-256 token document ID in both native token refresh and foreground registration. Native onNewToken refreshes the signed-in user's registration. The push relay reads past duplicate documents before selecting two distinct devices, and the caller retries when every attempted registration was rejected and pruned. Existing authentication, block and notification preferences remain enforced.

Validation completed locally: 184 Node tests passed across game engine, live moderation and call push; assembly patch applied successfully and a second application was idempotent; Python syntax and git diff whitespace checks passed.

Completed on Actions run 41110486403 at source e9fe66729db9727710963eedb8ebb4558bc73156: Flutter analysis, 70 application tests, reference-screen interaction checks, signed ARM64 APK compilation and signing-certificate verification. The APK artifact was finalized before the workflow was canceled during post-build cleanup by a workflow-only follow-up. The follow-up bounds NDK download time and does not change the application runtime.

APK: `NgelX-1.0.355-Build585-REVIEW.apk` (50,220,533 bytes), package `com.nnentx.ngelx_app`, versionName `1.0.355`, versionCode `585`.
SHA-256: `a2bfe028ab4f63c1b44a36083081c89827793a92575fb404cc3d5a3e6f26eb7d`.
Signing certificate SHA-256: `be20b27f0ba1f4decd2941d410b1536de89e48dc894f04f038f9d26b11ecd6aa`.
Artifact ID: `13004356404`. Local verification matched the artifact ZIP digest and APK digest, decoded the packaged Android manifest, validated archive integrity, and checked ARM64 app content and absence of demo ad identifiers. The new controls screenshot was inspected with actual fonts.

Pending: two-phone background/locked-screen voice/video calling in both directions. The push relay changes are prepared and tested but have not been deployed. No production worker or in-app updater was changed.

The user explicitly approved sending this implementation to the Nnentx/Ngelx repository and building the review APK. The change is prepared on a separate review branch; it does not deploy production services or modify the in-app updater.
