#!/usr/bin/env python3
"""Build487 read-only regression tests, run after the historical build scripts."""
from pathlib import Path
import importlib.util

SCRIPT=Path("tools/apply_build487_one_incoming_surface.py")
spec=importlib.util.spec_from_file_location("call487", SCRIPT)
call487=importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(call487)


def verify():
    dart=call487.DART.read_text(encoding="utf-8")
    service=call487.SERVICE.read_text(encoding="utf-8")
    assert call487.patch_dart(dart)==dart, "Flutter apply must be idempotent"
    assert call487.patch_service(service)==service, "Native apply must be idempotent"
    assert dart.count(call487.MARKER)==1
    assert "Widget _gelenAramaFlutterFallback487()" in dart
    assert "permission.data!.isGranted" in dart
    assert "kIsWeb" in dart and "TargetPlatform.android" in dart
    assert "_gelenAramaButon(" in dart and "Widget _gelenAramaFlutterFallback487()" in dart
    # One channel, silent system notification, original managed Ringtone.
    assert service.count("ngelx_incoming_calls487_one_ring")==1
    assert "channel.setSound(null, null)" in service
    assert "channel.enableVibration(false)" in service
    assert ".setSound(null)" in service
    assert ".setSound(ringtone" not in service
    assert "channel.setSound(ringtone" not in service
    assert "notification.flags = notification.flags or Notification.FLAG_INSISTENT" not in service
    for guard in ("sound.play()", "if(alerts.containsKey(room))", "ringing.remove(room)",
                  "setFullScreenIntent(fullScreenCall, true)", "fun isStillRinging470(room:",
                  "manager.notify(room.hashCode(), notification)",
                  "manager.currentInterruptionFilter",
                  "cancel(application, room)"):
        assert guard in service, "call system guard was lost: "+guard
    # The existing mini-call overlay must remain and must not be implemented
    # as a second room or replaced by the incoming visual surface.
    mini=Path("app/lib/build445_inbox_model.dart").read_text(encoding="utf-8")
    assert "class Ngelx445CallOverlay" in mini
    assert "ngelx445ReturnCall(name)" in mini
    assert "onPanUpdate:" in mini
    assert "ngelx445EndBackground(name)" in mini
    print("Build487 source regression: one call UI and one native ringtone owner PASS")


if __name__=="__main__":
    verify()
