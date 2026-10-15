# Build 463: intermittent user-photo / feed-video device reproduction (2026-10-15)

Source: user-provided 65-second on-device screen recording. **Do not upload or redistribute the video**; may contain private profiles, account identifiers and chat metadata.

## Direct visual evidence (approximate recording offsets)
- 00-24 s: transition to OS photo gallery and intermittently black/protected-recording screen with Android screenshot blocking toast; **not sufficient evidence of a NgelX media-picker defect**.
- 24 s: inbox shows several conversation/profile photos normally.
- 32-38 s: app switched away, restarted, inbox reopened; multiple circle avatars that previously showed images are now empty.
- 46 s and 54 s: feed frame is black with long-lived circular buffering / loading indicators.
- 48 s: profile avatar loads, introductory video preview appears as grey loading tile. Cover area blank; the video alone does not establish whether a cover was configured on that profile.
- 56-60 s: inbox shows mixed photo state, many circular placeholders, and "Kişi bilgisi yükleniyor..." on rows.
- 62-64 s: another profile image and intro thumbnail render. This confirms media visibility is intermittent across screens, not simply a single permanently missing image.

## Direct code findings (Build 463 / baseline code)
1. `_ngelxAgResmiBaytlari` in `app/lib/main.dart` used 3 requests for **each** alternate media host, 45-second receive timeout, a fresh Dio object per attempt, and mandatory `Cache-Control: no-cache, no-store` on every image. It had no shared in-flight deduplication and only an in-memory cache, which is discarded when the app restarts.
2. For known NgelX media hosts, `ngelxMedyaUrlAdaylari` prefers primary/secondary domains even when the saved photo URL is on a legacy domain; alternate host failures can delay the real host unnecessarily.
3. The inbox directly paints `CircleAvatar(backgroundImage:NgelXAgImageProvider(...))` with `child:null`; on network/image-decoding failure the UI becomes a featureless empty circle.
4. The user-profile and Firestore record streams can independently lack current photo metadata on initial render; the recording does **not** provide enough evidence to determine whether the URL is missing from a document, whether a GET failed, or whether a video CDN returned invalid content.

## Proposed Build464 client-only mitigation
- Coalesce requests for the same URL, queue at most six independent image downloads, bound each queued download to ~28s, preserve the saved URL as the first candidate, avoid unauthenticated cache bypass.
- Persist only anonymously fetched and successfully decoded public photo bytes in an app-private bounded 3-day cache; authenticated image responses are **not** written to persistent cache.
- Do not forward Firebase bearer ID tokens to unknown third-party hosts.
- Replace three inbox empty-circle image patterns with a visible user/group icon beneath a network image.
- Do **not** mutate Firestore documents, user profiles, groups, chat history, storage or production Firestore rules.
- These changes do **not** yet establish resolution of black feed videos or backend content availability.

## Acceptance criteria (real-device)
- On Build464 after an in-place install, inbox photo appears after first load and stays visible across two full app restarts on the same account, if the saved photo URL remains valid.
- 4G/5G transient disconnect produces a visible fallback icon, not an empty featureless circle; photos recover when internet returns.
- No regressions in cover-photo replacement, comment/post sending, chat history or Android signing.
- Record any persistent `Kişi bilgisi yükleniyor...` states separately; these are user metadata loads, not necessarily image bytes.
- Verify feed player error/timeout separately. **Do not claim black-feed-video bug fixed by an image-loader change.**
