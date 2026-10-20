Build546 continues the verified Build545 call/account handoff behavior.

Changes: reuse an already-connected room only when server-read guest acceptance and actual RTC media permissions permit it; otherwise fetch a new token before disconnecting. Guest membership and room/owner/identity are checked against server reads; leave/revoke stops both media tracks immediately, including late completion guards. Microphone readiness precedes camera capture, with bounded retries/manual retry, separate guest media controls, preserved reconnect preferences and optional voice-only guest entry. Recovery refreshes tokens instead of reusing a stale credential.

Native incoming calls load the exact groupPhotoUrl or caller profile photo asynchronously with the signed-in user's Firebase token. Requests are bounded and HTTPS media origins are allowlisted; identity/room/membership are checked and ringing/answer/reject never wait for an image. No new RTC room, local disk cache or server secret is introduced.

No billing/plan change, unrelated server deployment or production rule change is authorized by this workflow. Free-only constraint remains. Full live administrative moderation requires a working server endpoint and matching LiveKit administration credentials; availability is checked without printing values. Do not claim server moderation is active without deployment and end-to-end verification.

Target APK: com.nnentx.ngelx_app, 1.0.316 / Build546, original pinned signing certificate. Prior APKs/branches stay intact. Publish only the successfully checked bytes and then update ngelxsocial.com downloads. Physical two-device timing/audio and native photo acceptance remain required; source/unit tests do not establish handset latency.
