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
  and original failure propagation. Latest social patch awaits CI rerun.
- Local Flutter analysis remains unavailable because dependencies are absent;
  a metadata endpoint request rejected by automatic approval was not retried.
- No new APK, production backend deployment or phone regression yet.

## Remaining approved work

- Diagnose follow/friend request failures against deployed rules; preserve atomic
  request/notification creation and protect blocked pairs.
- Diagnose server quota errors in delete-for-everyone; do not promise removal of
  a provider quota and do not authorize billing changes.
- Group message pinning visibility investigation (current source already offers
  it to permitted members). Pending deduplication is implemented locally; the
  new emulator cases and coordinated deployment remain pending.
- Phone regression for founder transfer and follower search; rich shared-profile cards.
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
