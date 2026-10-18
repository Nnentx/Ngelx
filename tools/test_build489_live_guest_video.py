#!/usr/bin/env python3
"""Scoped Build489 generated-source guards; no production changes."""
from pathlib import Path
import importlib.util

spec=importlib.util.spec_from_file_location("build489","tools/apply_build489_live_guest_video.py")
assert spec and spec.loader
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def main():
    source=Path("app/lib/live_broadcast_studio.dart").read_text(encoding="utf-8")
    assert m.transform(source)==source, "Patch must be idempotent"
    body=source[source.index("class _CanliYayinPageState"):]
    assert body.count(m.MARKER)==1
    required=(
      "lk.VideoTrack? _guestVideo489(",
      "lk.VideoTrackRenderer(track,fit:lk.VideoViewFit.cover)",
      "_viewerGuestIds489()",
      "participant.videoTrackPublications.any(",
      "if(widget.yayinSahibi){",
      ".collection('guest_requests').snapshots()",
      "d.data()['status']=='accepted'",
      ".take(10).toList()",
      "Icons.add_rounded",
      "_guestRailOpen488",
      "PopupMenuButton<String>(",
      "'guestAudioMutedUids'",
      "FirebaseAuth.instance.currentUser?.uid!=widget.ownerId",
      "ng elx-placeholder",
      "tx.update(liveRef,",
      "accepted&&!_guestAudioMuted489",
      "_guestAudioPolicySub489?.cancel()",
      "Future<void>.value()",
      "MediaQuery.sizeOf(context).height*.37",
      "math.min(MediaQuery.sizeOf(context).height*.33",
      "_guestControl453(true)","_guestControl453(false)",
      "_yorumPaneli()","_hearts453","_kalpDegistir()",
    )
    for token in required:
        if token=="ng elx-placeholder":token="ngelx448GuestAction(context,widget.belgeId,widget.ownerId,uid,'reject')"
        assert token in body, token
    # Audience never enumerates protected guest_requests; owner-only branch
    # must contain the collection query.
    i=body.index("if(widget.yayinSahibi){",body.index("  Widget _guestRail488(){"))
    j=body.index("final ids=_viewerGuestIds489()",i)
    assert ".collection('guest_requests').snapshots()" in body[i:j]
    assert ".collection('guest_requests')" not in body[j:body.index("  Widget _yorumPaneli(){",j)]
    assert body.count("await widget.oda.localParticipant?.setMicrophoneEnabled(accepted&&!_guestAudioMuted489);")>=2
    # Build502: remote permission unmute NEVER turns on another person's mic.
    assert "if(changed&&muted&&_guestActive448){" in body
    assert "setMicrophoneEnabled(false) ?? Future<void>.value()" in body
    assert "setMicrophoneEnabled(!muted)" not in body
    assert "The guest controls when to unmute" in body
    print("Build489 B2 guards: real video, host-only guest list, scoped mute/kick and 10-tile layout PASS")


if __name__=="__main__":main()
