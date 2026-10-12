# Build444 call follow-up

46568 shows an ongoing voice-call banner while a feed video plays and other chat call buttons remain available. Several other recordings are black under capture protection; audible dropout has not been independently verified from those recordings.

Changes: reserve a single process-wide call before outgoing or incoming signaling; retain ownership while minimized; cancel late connection completion after hangup; close local room before Firestore writes; serialize explicit reconnects and retain microphone/camera/speaker choices; pause/block non-call media while a call owns audio; synthesized outgoing ringback stops on acceptance/end/error.

Required two-device checks: private voice/video, group calls, minimized call plus second-contact call attempt, feed playback during call, offline hangup, hangup during permission/token/connect, reconnect with microphone muted and Bluetooth connected, outgoing ringback until accept/reject/no-answer. Server/network packet loss cannot be declared fixed by client unit tests. Build443 profile capture propagation/default and English UI findings remain separate unfinished follow-ups.
