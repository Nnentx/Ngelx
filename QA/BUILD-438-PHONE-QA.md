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

- Added authenticated external account deletion and support forms. Deletion uses
  the existing user + account_deletion_requests records in one transaction,
  preserves an existing scheduled deadline, and supports a new request after
  cancellation. Support uses existing support_requests and returns a request ID.
  Passwords are not stored in request payloads; sign-in is kept in memory. These
  web forms currently require an email/password account session; no unauthenticated
  support channel or provider/SMS sign-in is claimed.
- Both forms use white styling, explicit deletion consent, colored status messages,
  disabled submission when the SDK fails, and no success before server confirmation.
- Actual website source is Nnentx/ngelx-web (CNAME ngelxsocial.com), separate from
  app repository. All six publish writes returned integration FORBIDDEN/403; no
  live website files changed. Repository access must be extended to publish.

## Validation so far

- Server username ownership now uses a shared transaction for index and profile,
  protects legacy unindexed owners, rejects conflicts, supports same-owner retry
  and retires previous names after rename. Read-only migration planning reports
  duplicate/invalid names without selecting an owner. 40 unit cases pass locally;
  emulator run 38137418637 passed on commit
  53fa7d4baa326fc843f2aa0c4af9a7271100cb9d: 10 concurrent claimants produce
  one owner; retry, atomic rename, retired-name protection, legacy owner
  protection and duplicate rejection passed. This is not
  yet routed from registration; direct username writes in existing rules require
  a coordinated migration/client/rules deployment. No production profile changed.

- Login groundwork now has 16 standalone Dart input cases and 28 server unit
  tests. Server core and Firebase Admin/REST adapters are committed separately
  under server/auth. Tests use fake adapters/upstream responses, not real
  accounts. App Check, private active username index, UID matching, linked phone
  provider, MFA/tenant rejection and password request/body deadlines are covered.
  No endpoint is deployed or connected to Flutter. Distributed throttling,
  server configuration, username migration/ownership and integration QA remain.
- Added distributed Firestore login counters: HMAC identifier/network keys,
  atomic all-or-none increments, 5/30 attempts per 60-second window, explicit
  trusted remote address, IPv6 normalization and failure-closed storage errors.
  All 36 server unit cases pass locally. Real emulator concurrency added to
  auth CI run 38132186576 passed on commit
  879034d668a657c81c69a188f4790252037a03af: simultaneous 20 requests admit
  exactly 5, cross-account network limit admits 3 of 10, expiry and hashed
  record privacy pass. These tests used demo-ngelx-auth, not production. No production
  counters, TTL policy, secret installation or endpoint deployment occurred.

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

- Web validation run 38128327785 passed on commit
  fe7b191f4c754b5a613b5e2f9d8583ab4014ddae, using the active production rule
  snapshot in an emulator: atomic deletion, preserved repeated-request deadline,
  cancelled requeue, concurrent requests, owner-only writes and support privacy.
- Browser tests passed at 360px and 1280px with fake SDK modules: no horizontal
  overflow, mandatory deletion consent, cleared password input, success states
  and disabled form on SDK load failure. These were not live-account browser tests.

## Remaining approved work

### Closed phone test round — 2026-10-11, 19:20 Europe/Istanbul

`apply_build438_message_round.py`: pinned rows return message IDs to the existing
chat jump (including group-info route); video previews use the bounded video
preview/thumbnail resolver rather than treating video URLs as images. Private
forwarded bubbles display a marker. Both approval paths now commit request state,
membership and one system event atomically, checking current admin role/capacity;
each invocation allocates its own event ID before the transaction; request-state retries ensure one winner without attempting to overwrite another invocation’s immutable system event.
CI 38156090812 passed on cd300b1f5d817586e8d7f019e51939092d4811f3:
Flutter analysis, existing app tests and full emulator suite succeeded.

`apply_build438_former_inbox.py`: former groups join inbox results; previews and
sorting freeze at exit rather than displaying future lastMessage/update time.
Voluntary leave no longer auto-archives. Existing read-only panel and server
message cutoff remain. New emulator cases cover pre/post-exit reads, denied
send/call and concurrent approval. Earlier closed-round CI runs failed the concurrent approval case; diagnostic single writes passed. The latest event-ID correction is undergoing full CI.
The twelve-language catalog now contains all 259 existing keys in every language; no new signed APK or production
deployment is claimed.

Follow-up patch `tools/apply_build438_inbox_round.py` now applies pinned-first
sorting to the unified All inbox, bounds preference writes and reports failures.
Mute membership/deadline changes are atomic; nested deadline maps replace dotted
keys used with set(merge) in chat-info controls. This repairs concrete code issues,
but does not prove the phone unmute symptom is resolved.
Archive loading retains one future across rebuilds, isolates failed legacy group
queries/inaccessible records from manual archives, exposes partial-result warnings
and retries, and never labels load failures as an empty archive. Archive write and
restore still need emulator/phone confirmation. Dart parsing and repeated patch
idempotence pass; full Flutter analysis is still pending. No APK or deployment.

User closed the Build437 phone round; do not request further baseline tests.
Confirmed by screenshots/report: read receipts, private/group search and reply
jumps, shared emoji, media, edits, forwarding delivery, block/unblock with old
history retained, restriction, follow/friend acceptance, group removal, member
search, founder transfer, shared-profile navigation, reset/verification emails,
mark-read counters, follower filtering/clear and removal (2 -> 1), typing.
These are phone observations, not proof of new Build438 code or all security paths.

Consolidated remaining defects/requests:
- Archive action leaves archive list empty; restore must be verified after fix.
- Pinning Selma does not move her above notifications/newer chats in All inbox.
- Mute suppresses sound; unmute does not restore it. Another never-muted chat
  produces sound/vibration, isolating the observed symptom to the muted chat.
- Follower search filters correctly, but keyboard intermittently loses focus.
- Group pinned-message rows do not jump; video preview fails; top bar occasionally
  becomes inconsistent after unpinning, then recovers.
- Approved member joins can send, but member-added system event is missing.
- Removed AND voluntarily departing members retain inbox entry and pre-exit
  history. Show removal actor or leave event and read-only explanation with
  delete-conversation action. Deny all future messages and calls until re-added;
  enforce history cutoff server-side. Preserve existing retention policy.
- Forwarded media arrives and opens; add forwarded marker inside message bubble.
- Keep all controls below status bar/notch, preserving feed layout.
- User requested 12 total languages: tr, en, de, ar, ru, ku (Kurmanci),
  zh (Simplified), hi, fr, es, it, pt. Preserve Arabic RTL and Kurmanci LTR.
  All 259 existing keyed UI strings now have seven new translations, the animated
  welcome is translated, and existing preference persistence is retained.
  Local Dart compilation, all-language catalog checks and patch idempotence pass.
  Existing uncatalogued/hardcoded screens still require localization work; no
  claim that every app string or user-generated content has been translated.
  Firebase Kurmanci emails explicitly use English; Chinese maps to zh-CN,
  Portuguese to pt-BR. No provider-side email template was changed.
- Investigate seen=1/delivered=0 semantics before calling it a counter defect.

Preserve deleted-message tombstones (explicitly approved), current themes,
working behavior and existing pending changes. No new APK is delivered yet.

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
- Publish tested external deletion/support forms to Nnentx/ngelx-web once the
  connected GitHub integration can write that repository; then live-account
  regression. A channel for users unable to authenticate still needs configuration.
- Full build/regression checks and signed consolidated APK after remaining fixes.

## Phone regression baseline to preserve

Media/text/voice, shared emoji/background, reactions, edits, own-side deletion,
search jump, unread/read behavior, forwarding, profile/group navigation,
password reset, recovery field persistence, account freeze/deletion undo,
blocking and two-way delivery after unblock, restriction-list persistence and
delivery after removing restriction all have phone evidence. Calls, background
push, remote logout, real recovery, permanent deletion and cleanup remain
unverified; they must not be marked passed.


### Current validation gate

CI 38157314387 passed analysis/app tests but failed concurrent approval after all
three isolated admin writes succeeded. Unique event document IDs per invocation
now prevent concurrent attempts from being evaluated as forbidden updates to an
existing system event, while request/version checks retain atomicity. This is
still a hypothesis until the updated concurrent emulator case passes. The
metadata comparison optimizer protects the same field set, with stricter
missing-vs-explicit-default handling. No production rules deployment.

The exact 12-language request overrides an earlier 14-language planning note.
Language catalog source lives in tools/build438_locales.tsv; the reproducible
patch preserves the original five translations. Full app CI is running on
91c8b0b1d3a362fccb87000809726372aa3fc8cf. No new APK delivered yet.


Full validation CI 38157978969 succeeded on 91c8b0b1d3a362fccb87000809726372aa3fc8cf:
12-language catalog compile/coverage, Flutter analysis, 33 app tests and full
Firestore suite including concurrent approval and former-member cutoff passed.
The event ID correction is validated; no security permission was widened.
A separate candidate workflow builds 1.0.213+438 with the exact existing
install-compatible test certificate, after all checks. It contains no production
rules, server or website deployment. Candidate APK is not a claim of full
uncatalogued-screen translation or phone confirmation of archive/unmute/focus.


### Build438 candidate artifact — 2026-10-11 17:19 UTC

CI 38158230552 succeeded on b4afc2673ddddad241c55d9c931b3b00314a8a82.
All catalog checks, Flutter analysis, 33 app tests and full Firestore tests passed
before Android release-mode compilation. APK version/build: 1.0.213 / 438.
APK size: 145,576,802 bytes.
APK SHA-256: e99cecf04fb7da78178def16baaaf93110b0a1c3c7b975d4f2a813ecb4bb6de2.
Verified V2 certificate SHA-256:
be20b27f0ba1f4decd2941d410b1536de89e48dc894f04f038f9d26b11ecd6aa.
This matches the installed Build437 test certificate. Downloaded archive and APK
checksums verified locally. No production deployment occurred. Current language
coverage extends the existing keyed catalog; uncatalogued hardcoded texts remain.
The user's closed Build437 test round stays closed.

### Screen localization follow-up — 2026-10-11

Attachment 46247.mp4 shows mixed-language UI: the French login retains a Turkish
welcome title, and the Kurmanci profile retains Turkish friends/intro/highlights,
story tab and post-menu labels. This is localization evidence only; the closed
phone QA round remains closed.

`apply_build438_screen_locales.py`, applied after `apply_build438_locales.py`,
connects 235 presentation literals to the existing catalog or 46 additional
12-language screen rows (including two spelling/capitalization aliases). It
localizes Text data and selected display-only properties/helpers; storage values,
Firestore field names, routes and user content are not rewritten. Constant
ancestors of runtime translations are removed selectively. The welcome widget
is no longer const, so selecting another language rebuilds its split title.
Existing Arabic direction handling and Kurmanci LTR remain unchanged.

Both validation and candidate workflows apply this reproducible patch. Local
Python checks confirm idempotence and separation of display literals from stored
values. Dart/Flutter are absent locally; CI compilation and app/security checks
are required before marking this patch validated. The previous candidate APK
and its checksum are unchanged. Additional uncatalogued screens, interpolated
status text and inline `lt` strings outside this catalog remain localization work;
this is not a claim of complete app-wide translation or a new delivered APK.
