# Build549: incoming call admission and quota pressure

Base: verified Build548 source bc8d2013b005af1b5b9ef428d210dfb82417c08a, run 39499920852.

Device screenshots show Firestore resource-exhausted (quota exceeded), a blocked pending self-leave, and a group invite that does not respond. The exact exhausted read/write quota cannot be inferred from those images. Client changes do not raise or reset the backend quota. No billing or infrastructure changes.

- Native answer accepts a current ringing private call or current active/ringing group invite. Server membership, room, age, kick and exit markers are rechecked inside the transaction. Rejecting a group invitation is local and never terminates other participants. Account changes and pending reservation cleanup remain guarded. Errors are shown instead of swallowed.
- Shared heartbeat gate deduplicates foreground/background requests, uses a 60-second per-device interval and skips writes when another participant refreshed within 50 seconds. Quota failures back off 120 seconds; no terminal status or membership is written by heartbeat. Failed heartbeat never tears down RTC.
- Pending self-leaves are preserved under quota; bulk replay stops on the first quota failure and retries are bounded to two minutes per key. A pending authoritative exit is never deleted merely to allow a join. Manual join reports the actual quota error rather than blaming connectivity.
- Private and group connection errors explain quota separately from microphone/camera permissions. Quota failure does not start the automatic reconnect loop. Group preflight reuses its initial snapshot instead of an immediate duplicate read. No cached data grants admission.

Validation: five source/lifecycle tests plus five Flutter policy tests, idempotent transform on the exact assembled Build548 source, full inherited regression chain, Flutter analysis and signed Android build. Physical two-device tests and actual backend quota availability remain separate acceptance criteria.
