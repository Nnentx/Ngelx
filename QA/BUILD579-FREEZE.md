# Build579: incoming invite freeze and false reconnect warning

The fallback pickup map in the inherited board painter used `for (...; i)` instead of incrementing `i`. With no initial room/power map, the very first paint entered an infinite synchronous loop on the UI isolate. Incoming chat invitations opened this state before the join request completed: both Join and Back appeared frozen. Prior full-room test stalls were this genuine defect; treating those stalls as environmental was incorrect.

The fallback is now a constant six-entry map. The real invite card, pending join route, joined room and Back transitions are covered by bounded Flutter tests. Busy/loading routes can close without pretending the server confirmed a leave. The card title fits its container at wider text metrics.

The reconnect button previously represented every gameplay error. An in-flight poll could also race a mutation: its fresh revision was discarded and the action sent with an old revision. Mutations now drain an existing poll before taking its revision. Sync revision conflicts retry at most three times. Conflicting manual moves/rolls are NEVER replayed; the authoritative room is refreshed instead. Gameplay rejections retain their real message. Established rooms show reconnect only after repeated transport failures; successful responses clear the warning. Initial joins can show retry after one connection failure. Poll backoff counts transport failures rather than arbitrary UI notifications.

Build identity: 1.0.349+579. Tested app source: 2208838b2fe50d2b5addb3dd9d07c2bad9ac7d16. Android run: 40386052388. Publication is gated on exact CI success and the unchanged Build578 live-accepted backend. No server deployment is required for this client-only correction. The in-app feed must change only after exact public APK bytes are verified.

Physical two-phone acceptance has not been performed. Automated tests must not be presented as that acceptance. Existing game layout, pawns, sound, wallet, XP and Auto features remain in the additive source patch.
