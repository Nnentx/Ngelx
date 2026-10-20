# Build547: Build546 device feedback

Base: verified Build546 assembled source from run 39446648099, commit 53c60d1a9752c56a2b8fb49d0634e4ea0b875879. Assembled artifact SHA256: 922bbe97f44498ffcc2d2b6048edf8314a447c2d56dcc4ff11eb0c30ec92233f.

- Keşfet reads canonical friend/follow outgoing records instead of a truncated notifications query. Existing friendships also use the active friendship record and either user's friends array, consistent with the profile. Pending requests remain pending after duplicate-send rejection. In-flight sends cannot be repeated; listeners are disposed and reject callbacks for another account.
- Removes only the redundant blue ongoing-call banner from private chats. Global return control, mini call window, history, answer/reject, audio session and group behavior remain intact.
- Native incoming screen loads an account/chat-scoped disk avatar independently of authenticated remote refresh. Flutter reuses already cached group/contact images without extra downloads or server queries. Successfully fetched native images are cached, bounded to 80 files, 512px decode, 2MiB inputs and 24h freshness. Cache miss/first unknown caller still depends on the network; instant first-ever remote photos cannot be guaranteed.
- Build546 live guest continuity fixes and all other generated source remain unchanged. No database rules or production service changes are part of Build547.

Validation: transformations applied twice against the exact Build546 assembled artifact; four new regression tests and three Build546 photo/live-source tests passed. Full Flutter analysis, Android build, signing and device verification remain pending until CI succeeds.

Device acceptance: Rüzgar already-friend state agrees between profile and Keşfet; pending request remains disabled after repeated taps, even with >100 newer notifications; cancellation/rejection refreshes state; private/group call avatar appears quickly on warm cache; cache miss never delays ring/answer; no blue private-chat call banner; existing global return and mini window work; guest audio/video and mute continue working.
