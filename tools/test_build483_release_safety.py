#!/usr/bin/env python3
"""Build483 safety checks with in-memory fake Firebase Rules API only.

No network, credentials, Firestore documents or live rules are accessed.
These tests validate the release script's abort, verify and rollback paths.
"""
import sys
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import release_build483_production_rules as release


OLD = release.RELEASE.replace("/releases/cloud.firestore", "/rulesets/previous")
NEW = release.RELEASE.replace("/releases/cloud.firestore", "/rulesets/candidate")


class FakeResponse:
    def __init__(self, body, code=200):
        self.body = body
        self.status_code = code
        self.ok = 200 <= code < 300

    def json(self):
        return self.body


class FakeRules:
    def __init__(self, old="before", new="after", current=OLD):
        self.previous = old
        self.candidate = new
        self.current = current
        self.post_calls = 0
        self.patch_calls = []
        self.wrong_readback = False

    def post(self, url, json, timeout):
        self.post_calls += 1
        assert url.endswith("/rulesets")
        assert json["source"]["files"][0]["content"] == self.candidate
        return FakeResponse({"name": NEW})

    def patch(self, url, json, timeout):
        assert url == release.RULE_API + release.RELEASE
        assert json["release"]["name"] == release.RELEASE
        target = json["release"]["rulesetName"]
        assert target in (OLD, NEW)
        self.patch_calls.append(target)
        self.current = target
        return FakeResponse({"name": release.RELEASE, "rulesetName": target})


class Build483ReleaseSafetyTests(unittest.TestCase):
    def setup_fake(self, fake):
        # Patch all requests at the release-script boundary, not Firebase itself.
        context = [
            patch.object(release, "session", return_value=fake),
            patch.object(release, "validate_bundle", return_value=(
                {"rulesetName": OLD}, fake.previous, fake.candidate
            )),
            patch.object(release, "read_release", side_effect=lambda http: {
                "name": release.RELEASE, "rulesetName": http.current
            }),
            patch.object(release, "read_ruleset", side_effect=lambda http, ref:
                http.previous if ref == OLD
                else (http.candidate + "-drift" if http.wrong_readback and
                      http.current == NEW else http.candidate)),
            patch.object(release.time, "sleep", return_value=None),
        ]
        for item in context:
            item.start()
            self.addCleanup(item.stop)

    def test_successful_release_updates_only_ruleset_pointer(self):
        fake = FakeRules()
        self.setup_fake(fake)
        release.publish()
        self.assertEqual(fake.current, NEW)
        self.assertEqual(fake.patch_calls, [NEW])
        self.assertEqual(fake.post_calls, 1)

    def test_changed_live_release_aborts_before_any_write(self):
        fake = FakeRules(current=release.RELEASE.replace(
            "/releases/cloud.firestore", "/rulesets/other"))
        self.setup_fake(fake)
        with self.assertRaisesRegex(RuntimeError, "changed after QA"):
            release.publish()
        self.assertEqual(fake.post_calls, 0)
        self.assertEqual(fake.patch_calls, [])

    def test_tampered_candidate_aborts_before_release_patch(self):
        fake = FakeRules()
        self.setup_fake(fake)
        with patch.object(release, "read_ruleset",
                          side_effect=lambda http, ref:
                          fake.previous if ref == OLD else "tampered"):
            with self.assertRaisesRegex(RuntimeError, "differs from test"):
                release.publish()
        self.assertEqual(fake.current, OLD)
        self.assertEqual(fake.patch_calls, [])

    def test_post_publish_readback_error_rolls_back_previous_ruleset(self):
        fake = FakeRules()
        fake.wrong_readback = True
        self.setup_fake(fake)
        # A bad read-back after PATCH must restore the known previous release.
        # During immutable-candidate creation, the same candidate is valid.
        original_reader = release.read_ruleset
        attempts = {"new": 0}

        def reader(http, ref):
            if ref == OLD:
                return fake.previous
            attempts["new"] += 1
            if attempts["new"] == 1:
                return fake.candidate
            return fake.candidate + "-mismatch"

        with patch.object(release, "read_ruleset", side_effect=reader):
            with self.assertRaisesRegex(RuntimeError, "verification failed"):
                release.publish()
        self.assertEqual(fake.current, OLD)
        self.assertEqual(fake.patch_calls, [NEW, OLD])

    def test_read_only_stage_saves_exact_rollback_and_candidate(self):
        fake = FakeRules(old="production rules", new="candidate rules")
        with tempfile.TemporaryDirectory() as temp:
            previous = os.getcwd()
            os.chdir(temp)
            try:
                bundle = Path("build483-rollback")
                with (
                    patch.object(release, "session", return_value=fake),
                    patch.object(release, "read_release",
                                 return_value={"name": release.RELEASE,
                                               "rulesetName": OLD}),
                    patch.object(release, "read_ruleset",
                                 return_value=fake.previous),
                    patch.object(release, "prepare_production_candidate",
                                 return_value=fake.candidate),
                    patch.object(release, "BASE_HASH",
                                 release.digest(fake.previous)[:16]),
                    patch.object(release, "QA_HASH",
                                 release.digest(fake.candidate)[:16]),
                ):
                    release.stage()
                    self.assertEqual(
                        (bundle / "previous.rules").read_text(),
                        fake.previous,
                    )
                    self.assertEqual(
                        (bundle / "candidate.rules").read_text(),
                        fake.candidate,
                    )
                    self.assertEqual(Path("firestore.rules").read_text(),
                                     fake.candidate)
                    release.validate_bundle()
                    (bundle / "candidate.rules").write_text("tampered")
                    with self.assertRaisesRegex(
                        RuntimeError, "checksum mismatch"
                    ):
                        release.validate_bundle()
                self.assertEqual(fake.post_calls, 0)
                self.assertEqual(fake.patch_calls, [])
            finally:
                os.chdir(previous)

    def test_read_only_stage_aborts_when_live_hash_changed(self):
        fake = FakeRules(old="unexpected production rules")
        with tempfile.TemporaryDirectory() as temp:
            previous = os.getcwd()
            os.chdir(temp)
            try:
                with (
                    patch.object(release, "session", return_value=fake),
                    patch.object(release, "read_release",
                                 return_value={"name": release.RELEASE,
                                               "rulesetName": OLD}),
                    patch.object(release, "read_ruleset",
                                 return_value=fake.previous),
                ):
                    with self.assertRaisesRegex(
                        RuntimeError, "Production rules changed"
                    ):
                        release.stage()
                self.assertFalse(Path("build483-rollback").exists())
                self.assertEqual(fake.post_calls, 0)
                self.assertEqual(fake.patch_calls, [])
            finally:
                os.chdir(previous)

    def test_rejects_cross_project_ruleset(self):
        class Http:
            def patch(self, *args, **kwargs):
                self.fail("should not reach API")
        with self.assertRaisesRegex(RuntimeError, "Refusing unknown ruleset"):
            release.patch_release(Http(), "projects/another/rulesets/123")


if __name__ == "__main__":
    unittest.main()
