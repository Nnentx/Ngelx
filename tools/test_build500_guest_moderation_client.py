#!/usr/bin/env python3
"""Build500 QA: fail-closed authenticated host moderation bridge source guard."""
from pathlib import Path
import importlib.util
spec=importlib.util.spec_from_file_location("b500","tools/apply_build500_guest_moderation_client.py")
assert spec and spec.loader
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

def main():
    source=Path("app/lib/live_broadcast_studio.dart").read_text(encoding="utf-8")
    main_src=Path("app/lib/main.dart").read_text(encoding="utf-8")
    assert mod.transform_live(source)==source, "Build500 patch must be idempotent"
    assert mod.transform_main(main_src)==main_src, "Dio import must be idempotent"
    assert main_src.count("package:dio/dio.dart")==1

    begin=source.index("  Future<void> _hostGuestAction489(")
    end=source.index("  Widget _guestTile489(",begin)
    method=source[begin:end]
    for required in (
        mod.MARKER,
        "NGELX_LIVEKIT_GUEST_MODERATION_URL",
        "uri.scheme!='https'",
        "uri.userInfo.isNotEmpty",
        "uri.fragment.isNotEmpty",
        "Güvenli konuk yönetimi bu test sürümünde etkin değil.",
        "FirebaseAuth.instance.currentUser?.uid!=widget.ownerId",
        "_guestModerationPending500.contains(uid)",
        "final idToken=await user.getIdToken();",
        "'Authorization':'Bearer $idToken'",
        "'Content-Type':'application/json'",
        "'liveId':widget.belgeId,'guestUid':uid,'action':action",
        "connectTimeout:const Duration(seconds:8)",
        "receiveTimeout:const Duration(seconds:15)",
        "followRedirects:false",
        "response.statusCode!=200",
        "response.data['ok']!=true",
        "Konuk yönetimi sunucuda doğrulanamadı.",
        "finally{",
    ):
        assert required in method, required
    for banned in (
        "FirebaseFirestore.instance.runTransaction",
        "FieldValue.arrayUnion",
        "FieldValue.arrayRemove",
        "ngelx448GuestAction(context,widget.belgeId,widget.ownerId,uid,'reject')",
        "http://",
        "NGELX_LIVEKIT_TOKEN_URL",
    ):
        assert banned not in method, banned
    assert source.count(mod.MARKER)==1
    assert "_guestAudioPolicySub489" in source
    assert "_guestRail488()" in source
    assert "_hostGuestAction489" in source
    # Fail-fast guard against a changed original guest moderation block.
    try:
        mod.transform_live(source.replace(mod.MARKER,"// other marker"))
    except RuntimeError:
        pass
    else:
        raise AssertionError("Build500 must not silently patch an unexpected source version")
    # Missing Dio on unrelated generated test source is inserted at import boundary.
    sample="library test;\nimport 'dart:async';\nvoid main() {}\n"
    patched=mod.transform_main(sample)
    assert patched.startswith("library test;\nimport 'package:dio/dio.dart';\n")
    assert mod.transform_main(patched)==patched
    print("Build500 authenticated HTTPS-only, fail-closed host moderation bridge PASS")

if __name__=="__main__":
    main()
