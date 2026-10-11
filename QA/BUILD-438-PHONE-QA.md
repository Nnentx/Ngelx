# Build438 phone QA follow-up — implementation in progress

Scope approved on 2026-10-11: preserve working Build437 behavior, consolidate the
phone findings into one later release. This is not a release or a claim that all
46 items passed. Do not include cancelled chat drafts.

## Applied in the reproducible patch

Run `python3 tools/apply_build438_qa_fixes.py` **after** the existing Build437
generation steps. Generated app files already contain these changes locally;
the generated working tree predates this task and is not committed wholesale.

- Recreate the root auth route on login/logout instead of leaving a previous
  session's route alive. Bound profile cache/server reads. Phone regression still
  needed for first login after requesting account deletion.
- Restriction allows DM sending/profile-to-chat/story replies while the existing
  incoming notification filter stays active. Blocking and audience permission
  checks remain. The phone test previously proved restriction denied sending,
  contrary to its confirmation text. Notification silence must be tested.
- Quote previews in private/group messages invoke the existing bounded,
  access-aware search jump. Deleted/expired message handling stays shared.
- Recovery saved/restriction added or removed use the green success helper.
- Account freeze/delete dialogs explicitly use the white theme.
- Feed SafeArea prevents video rendering behind the system status bar.
- Remove standalone block/restrict/recovery entries from settings search; keep
  the combined block/restrict page and security recovery entry.
- Display the existing 3–20 character registration username limit.
- Three group exit paths now automatically transfer ownership after confirmation
  using the existing authorized transfer transaction. Existing admins take
  priority; otherwise member insertion order is used (explicit per-member join
  timestamps do not exist). Transfer failure prevents leaving. Transfer and exit
  are separate operations under current rules; a network failure between them
  may leave the old founder as an ordinary member. Retry must remain possible.
- Cache the follower/friend list stream and aggregate profile future across
  keystrokes so search rebuilds do not replace the focused input with a spinner.

- Group pending requests use a canonical target UID and a transaction so two
  members cannot overwrite or duplicate the same pending target. Current group
  members can list pending requests; outsiders remain denied. Rejected/cancelled
  requests can be resubmitted. This requires coordinated client/rules deployment.
  Added emulator cases for outsider access, overwrite denial and concurrent sends.

- Follow/friend transaction timeouts now reconcile the exact request generation
  and notification ID with a bounded server read. Confirmed requests report
  success; offline/uncertain results stay uncertain. Atomic request/notification
  writes and blocked-pair checks remain. This does not establish the root cause
  of the earlier phone request failures.

- Private shared-profile messages now render a white avatar/name/username card.
  New sends capture public identity fields after a server permission check;
  deactivated/blocked profiles and friends-only sharing remain guarded. Old
  messages fall back to their stored name/avatar placeholder. Tap still opens
  the existing profile route and its access checks. Phone layout needs testing.

- All four verification/reset email send paths explicitly set the selected app
  language (Turkish when the app is Turkish), with bounded calls. Previously only
  the forgot-password page set it. Firebase template branding, sender domain,
  deliverability and email action routing still require separate work. The existing
  web/reset-password.html already asks for the new password twice; its production
  hosting and Firebase email action URL remain unverified.

- Group pin menu defaults now match server permissions: missing setting means
  admins only. Menu refreshes group data with a bounded server read, using the
  existing cache offline. Pin/unpin writes read current role and message state in
  a transaction; removed admins cannot act on cached roles and simultaneous
  toggles retry against current state. Deleted messages cannot be newly pinned.
  Both menu and pinned-message page use the same transaction. Success uses green
  feedback and failures preserve permission/quota/uncertain-result information.

- Delete-for-everyone keeps the existing durable retry queue and exact media
  cleanup manifest required by rules. A second foreground attempt now reports
  that deletion is already running instead of falsely showing success. A session
  switch aborts that attempt. Successful deletions use green feedback; provider
  quota failures show an amber explanation that the pending request is retained
  on this device. Permission/other failures use red. This does not change quotas.

## Validation so far

- Dart parser/formatter (`--output=none`) accepted both changed Dart files.
- Reapplying the patch yields identical file hashes.
- Successor selection passed five standalone Dart scenarios: administrator
  priority, oldest member fallback, last member, stale admin and multiple admins.
- First isolated CI run 38120291868 passed on commit
  7e0a4c3f8c0d85c10bdff3e7f27e3f84a6fae626: Flutter analysis had no fatal
  errors (840 warning/info findings retained), all 33 app tests passed, and the
  full Firestore emulator suite including concurrent requests passed.
- Six standalone asynchronous confirmation scenarios passed: immediate success,
  already pending, confirmed timeout, unconfirmed timeout, offline confirmation,
  and original failure propagation. Final isolated CI run 38120975605 passed on
  commit 54d69949adbdcb871ca52ce1903bc64b4ca18467, including social confirmation,
  profile cards and account email language. All 33 app tests and the Firestore
  emulator suite passed again; analysis produced no fatal errors.
- Local Flutter analysis remains unavailable because dependencies are absent;
  a metadata endpoint request rejected by automatic approval was not retried.
- No new APK, production backend deployment or phone regression yet.

- Latest full CI run 38122742003 passed on commit
  66dfcdf772b4c65ae81232326d75ab9c29fb64fc: all 33 app tests, 19 standalone
  scenarios (including 8 pin permission cases), analysis with no fatal errors
  (845 warnings/info) and full Firestore emulator suite passed. Pin tests include
  concurrent toggles, revoked-admin denial, default permissions and outsider denial.
- Read-only diagnostic run 38122837410 passed against the active production
  rule snapshot SHA256 08dcd247ef3fc1087e238594993c53f5dd595ad8ea844cce89899cbaa6036493.
  Exact atomic social request/notification payloads work; recipient access,
  duplicate suppression and blocked-pair rollback passed in the emulator.
  No production account data read/written, rule deployment or cleanup occurred.
  This narrows the phone issue; actual account data, quotas and delivery remain
  unverified and the phone failure is not marked fixed.

## Remaining approved work

- Follow/friend phone regression: active-rule atomic writes passed the isolated
  diagnostic. Actual-account state, connectivity/quota and notification delivery
  still need diagnosis; protected blocked pairs remain unchanged.
- Diagnose server quota errors in delete-for-everyone; do not promise removal of
  a provider quota and do not authorize billing changes.
- Phone regression for updated group pin visibility and transactions. Pending
  request emulator cases passed; coordinated production deployment remains pending.
- Phone regression for founder transfer and follower search and shared-profile card layout.
- Other success/error/warning colors and timeout/error feedback.
- Email/username/verified-phone login with a secure identifier resolver. Do not
  expose account emails or trust unverified profile phone fields as credentials.
- Turkish branded verification/reset emails and repeat-password reset page;
  investigate deliverability without promising spam elimination.
- Actual external deletion request/support channel and correct website route
  instructions. No invented support address.
- Full build/regression checks and signed consolidated APK after remaining fixes.

## Phone regression baseline to preserve

Media/text/voice, shared emoji/background, reactions, edits, own-side deletion,
search jump, unread/read behavior, forwarding, profile/group navigation,
password reset, recovery field persistence, account freeze/deletion undo,
blocking and two-way delivery after unblock, restriction-list persistence and
delivery after removing restriction all have phone evidence. Calls, background
push, remote logout, real recovery, permanent deletion and cleanup remain
unverified; they must not be marked passed.
