Build546 continues the verified Build545 call/account handoff behavior.

Changes: reuse an already-connected room only when server-read guest acceptance and actual RTC media permissions permit it; otherwise fetch a new token before disconnecting. Guest membership and room/owner/identity are checked against server reads; leave/revoke stops both media tracks immediately, including late completion guards. Microphone readiness precedes camera capture, with bounded retries/manual retry, separate guest media controls, preserved reconnect preferences and optional voice-only guest entry. Recovery refreshes tokens instead of reusing a stale credential.

Native incoming calls load the exact groupPhotoUrl or caller profile photo asynchronously with the signed-in user's Firebase token. Requests are bounded and HTTPS media origins are allowlisted; identity/room/membership are checked and ringing/answer/reject never wait for an image. No new RTC room, local disk cache or server secret is introduced.

No billing/plan change, unrelated server deployment or production rule change is authorized by this workflow. Free-only constraint remains. Full live administrative moderation requires a working server endpoint and matching LiveKit administration credentials; availability is checked without printing values. Do not claim server moderation is active without deployment and end-to-end verification.

Target APK: com.nnentx.ngelx_app, 1.0.316 / Build546, original pinned signing certificate. Prior APKs/branches stay intact. Publish only the successfully checked bytes and then update ngelxsocial.com downloads. Physical two-device timing/audio and native photo acceptance remain required; source/unit tests do not establish handset latency.

Verified outcome (2026-10-20):
- Full run 39446648099 succeeded for source 53c60d1a9752c56a2b8fb49d0634e4ea0b875879: complete source regeneration, prior regressions, new guest policy/source gates, Flutter tests/analysis, Android native build, original signer and package/version checks.
- APK SHA256 f1dca2f3545c430322e0d4ccf98794fb498d007e039688589b3c29d5f1a7a33f, 46824895 bytes. Downloaded artifact digests, APK checksum/ZIP integrity and exact assembled-source transforms independently verified. Shared call join/departure/PiP source files are byte-identical to Build545.
- Public release v1.0.316-build546-test published in run 39449411979. Release API requires workflow write authority when the target differs from main's workflows, so release source snapshot a81919ca5d4e8fe9f0ee07bdee6c3228e860e0b9 preserves all tested app/tools/server trees but uses the trusted main workflow tree unchanged. See RELEASE546_MANIFEST.json. The APK was not rebuilt or altered.
- ngelxsocial.com/index.html updated in Nnentx/ngelx-web commit b0d84e12c0837d413e1bbb940169d07c4e27fec7. All three live APK links independently read back as Build546.
- Live administration remains blocked: build credentials absent; known Secret Manager resources returned HTTP403 under existing server identity in read-only run 39446949305. No paid services enabled. Recursive community delete remains inactive.
- Two-device admission timing, remote audio, camera-off/avatar and native incoming photo acceptance remain pending physical-device QA.
