# Build556 — community and chat feedback

Base: `qa/ngelx-free-live555-20261022`, commit `97d6b2459dcf85e74ed3ceedc1fea80d4fe9b9a6`. Apply after every existing Build395–554 generation step used by the Build555 candidate. The raw repository app is Build399; it must not be compiled as Build556 without that assembly. No production deployment or Android package was made in this task.

## Implemented source changes

| Feedback | Change / remaining validation |
| --- | --- |
| Inbox action menu overflows navigation | Scrollable full-height sheet with system safe area; device validation pending. |
| Mute, microphone, speaker and voice calls | Existing behavior preserved; 34 push/deletion policy tests pass. Actual two-device microphone, audio routing, mute expiry and ringing tests remain required. |
| Rear camera unavailable after turning video on in voice call | Camera-switch action is available when a local track exists, including private and group voice calls. Direction changes are serialized. Front/back device verification pending. |
| Ayaz / `@herkes` mentions | Immediate command suggestion, Turkish case folding, full member results and failed-profile retry. Existing mention permissions remain authoritative. |
| Pending friend requests reappear after update | Canonical request IDs override scoped legacy pending notifications. Existing outgoing requests no longer depend solely on legacy notification history. Verify migration, cancellation and account switching against actual records. |
| Community delete error | Endpoint returned HTTP 404 during read-only diagnosis. Client distinguishes missing service from ambiguous failure. Existing authenticated founder-only recursive-delete policy remains unchanged. **Actual deletion remains blocked by missing deployed service; no claim of repair or successful deletion.** |
| Comment counter remains zero | Refresh is triggered on comment create/delete and when closing the comment sheet. Verify across two accounts; no new unbounded counter listener. |
| Community notifications | New approved posts, pending posts, membership requests and comments produce existing Activity notifications with community name and a small “Topluluk” label; taps open the community. Delivery depends on existing permissions/preferences and network. Scheduled posts and subsequent moderator-approval notifications require backend delivery follow-up. |
| Internal sharing | Share menu offers NgelX conversations and external apps. Picker includes private/group chats. Current membership, private-community audience, block/privacy, group admin-only posting and message expiry are checked before atomic delivery. Repeated attempts reuse a message ID. A clickable community card is rendered in private and group messages. |
| Manual community refresh | Pull-to-refresh requests current approved posts and community data, then renews the live feed; empty feed remains scrollable. |
| Community create/admin design | Cover/avatar preview, ordered information/privacy sections, readable settings dialog and aligned admin rows with pending badges. Keyboard/large-text widget tests added, not executed. |
| Intermittent gray community blocks | Hardened missing author fields and invalid legacy timestamps, plus refresh recovery. **Cause and resolution are not device-verified.** Capture Flutter exception and affected record if it recurs. |
| Intro video sound overlay | Removed floating speaker icon; existing playback controls retained. |
| Highlights invisible to visitors / removal | Added visitor highlight list behind existing profile-access gate, individual story privacy and hidden-audience checks. Live query removes deleted/unhighlighted items. Twelve standalone policy checks pass. |
| Chat opens at old messages | Opening scroll waits for nonempty messages; bounded retry tolerates slower content layout and stops on history interaction. Deep-link message navigation is preserved. |

## Validation performed

- Dart formatter parsed all six changed/new Dart source files without syntax errors; this is not a type-check.
- `dart tools/build556_policy_test.dart`: 12 policy checks passed.
- `node --test server/community543/delete-policy.test.mjs cloudflare/call-push/test/push.test.mjs`: 34 tests passed.
- `python3 tools/test_build556_quality.py`: cold apply, repeat apply, exact generated-source hashes and fail-before-write drift guard passed.
- Reapplied the package against the exact local assembled Build555 baseline and repeated it successfully.
- Flutter package fetch was blocked by automatic security review because the fetch process attempted cloud metadata access at `169.254.169.254`. It was not retried through an alternative route. Full Flutter analysis, widget tests, APK build and actual-device acceptance remain **not run**.

## Integration

1. Use the existing Build555 source-generation pipeline with its original ordering, isolated legacy rules fixture and restored modern rules. Do not skip prior generation steps.
2. Run `python3 tools/apply_build556_quality.py` after `tools/apply_build554_live_fixes.py` and before Flutter analysis/build. The guard rejects a different or partially changed baseline instead of overwriting it.
3. Copy `tools/build556_widget_test.dart` to `app/test/build556_widget_test.dart`, then run the standalone policy test, package regression test, full Flutter analysis and widget tests in an environment that does not attempt metadata access.
4. Run the existing signed Android candidate build using the next approved version. This package does not alter signing, production configuration, security rules, retention/cleanup pauses, websites or stored user data.
5. Restore/enable the existing community-delete service through the project's established backend deployment process, then verify unauthorized requests fail and a disposable founder-owned test community deletes fully. Do not test deletion against real user communities.
