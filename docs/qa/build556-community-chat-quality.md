# Build556 — community and chat feedback

Base: `qa/ngelx-free-live555-20261022`, commit `97d6b2459dcf85e74ed3ceedc1fea80d4fe9b9a6`. Apply after every existing Build395–554 generation step used by the Build555 candidate. The raw repository app is Build399; it must not be compiled as Build556 without that assembly. The follow-up adds an existing-worker deployment and signed Android candidate workflow. Deployment/build status must be verified from the workflow before claiming either completed.

## Implemented source changes

| Feedback | Change / remaining validation |
| --- | --- |
| Inbox action menu overflows navigation | Scrollable full-height sheet with system safe area; device validation pending. |
| Mute, microphone, speaker and voice calls | Existing behavior preserved; 34 push/deletion policy tests pass. Actual two-device microphone, audio routing, mute expiry and ringing tests remain required. |
| Rear camera unavailable after turning video on in voice call | Camera-switch action is available when a local track exists, including private and group voice calls. Direction changes are serialized. Front/back device verification pending. |
| Ayaz / `@herkes` mentions | Immediate command suggestion, Turkish case folding, full member results and failed-profile retry. Existing mention permissions remain authoritative. |
| Pending friend requests reappear after update | Canonical request IDs override scoped legacy pending notifications. Existing outgoing requests no longer depend solely on legacy notification history. Verify migration, cancellation and account switching against actual records. |
| Community delete error | Original Functions endpoint returned HTTP 404. Added `/community/delete` to the existing Worker with founder-only, exact-name confirmation, revoked/anonymous-token rejection, atomic owner receipts, expiring leases and bounded recursive chunks. The client persists owner-scoped confirmed jobs and resumes after interruption. Root/version protection prevents writes after deletion begins and protects recreated IDs. Deployment and authenticated device verification remain separate gates. |
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
- `node --test server/community543/delete-policy.test.mjs cloudflare/call-push/test/push.test.mjs`: 34 tests passed initially. Follow-up full moderation/auth/push/delete suite: **104 tests passed**, including eight new deletion adapter/ownership/resumption tests.
- `python3 tools/test_build556_quality.py`: cold apply, repeat apply, exact generated-source hashes and fail-before-write drift guard passed.
- Reapplied the package against the exact local assembled Build555 baseline and repeated it successfully.
- Local Flutter execution was blocked by automatic security review because it attempted cloud metadata access at `169.254.169.254`, including a follow-up version invocation. No metadata or credentials were accessed. The new workflow runs the existing Flutter build on GitHub instead; its actual outcome and device acceptance remain to be recorded.

## Integration

1. Use the existing Build555 source-generation pipeline with its original ordering, isolated legacy rules fixture and restored modern rules. Do not skip prior generation steps.
2. Run `python3 tools/apply_build556_quality.py` after `tools/apply_build554_live_fixes.py` and before Flutter analysis/build. The guard rejects a different or partially changed baseline instead of overwriting it.
3. Copy `tools/build556_widget_test.dart` to `app/test/build556_widget_test.dart`, then run the standalone policy test, package regression test, full Flutter analysis and widget tests in an environment that does not attempt metadata access.
4. Run the existing signed Android candidate build using the next approved version. This package does not alter signing, production configuration, security rules, retention/cleanup pauses, websites or stored user data.
5. Run `.github/workflows/NgelX-BUILD556-QUALITY.yml`: backend tests and verification must pass before the APK job starts. It redeploys only the existing configured Worker without changing secrets, bindings, subscriptions or billing. Verify anonymous requests fail, then let the owner verify a disposable founder-owned test community from the new app. Do not delete real communities merely to test.

## Follow-up implementation

- `cloudflare/live-moderation/src/community-delete.mjs`: existing authenticated service identity, exact community prefix checks, original-founder receipts, root document version precondition, bounded depth-first cleanup, no arbitrary media/user/chat deletion, and lease-safe retry. Chunk requests stay below the existing free Worker subrequest allowance.
- `app/lib/build556_delete.dart` is copied from `tools` during assembly. Only explicitly confirmed owner jobs enter preferences. The existing account-scoped pending-operation retry hook also resumes deletions; it never replays as another signed-in user.
- `tools/preflight_build556_worker.mjs` verifies the existing owner account, existing Worker and existing healthy configuration before redeploying. No secret values are written to artifacts or logs.
- Existing moderation paths and all earlier source-generation steps are retained.
