import datetime as dt
import unittest
from backup_metadata_readonly_audit import summarize_backups, summarize_lifecycle, summarize_pitr, PROJECT

UTC = dt.timezone.utc


class BackupMetadataSafetyTests(unittest.TestCase):
    def test_only_default_db_ready_backups_counted(self):
        payload = {"backups": [
            {"state": "READY", "database": f"projects/{PROJECT}/databases/(default)",
             "snapshotTime": "2026-10-14T00:00:00Z",
             "name": "projects/private/backup/SHOULD_NOT_BE_PRINTED"},
            {"state": "CREATING", "database": f"projects/{PROJECT}/databases/(default)"},
            {"state": "READY", "database": f"projects/{PROJECT}/databases/other"},
        ]}
        result = summarize_backups(payload, dt.datetime(2026, 10, 15, tzinfo=UTC))
        self.assertEqual(result["state"], "READY")
        self.assertEqual(result["ready_count"], 1)
        self.assertEqual(result["latest_snapshot_age_days"], 1)
        self.assertNotIn("SHOULD_NOT_BE_PRINTED", str(result))

    def test_partial_backup_listing_never_confirms_ready(self):
        payload = {"backups": [
            {"state": "READY", "database": f"projects/{PROJECT}/databases/(default)"}
        ], "unreachable": ["private-location"]}
        result = summarize_backups(payload)
        self.assertEqual(result["state"], "PARTIAL")
        self.assertEqual(result["unreachable_location_count"], 1)

    def test_pitr_enabled_can_cover_previous_cleanup_time(self):
        self.assertEqual(summarize_pitr({
            "pointInTimeRecoveryEnablement": "POINT_IN_TIME_RECOVERY_ENABLED",
            "earliestVersionTime": "2026-10-10T00:00:00Z",
        })["pre_cleanup_read_time_in_window"], True)

    def test_pitr_disabled_never_reports_recovery(self):
        result = summarize_pitr({
            "pointInTimeRecoveryEnablement": "POINT_IN_TIME_RECOVERY_DISABLED",
            "earliestVersionTime": "2026-10-10T00:00:00Z",
        })
        self.assertEqual(result["state"], "DISABLED")
        self.assertFalse(result["pre_cleanup_read_time_in_window"])

    def test_no_backups_is_not_a_success(self):
        self.assertEqual(summarize_backups({})["state"], "NONE")

    def test_r2_rule_summary_only_reports_counts_not_prefixes(self):
        response = {"result": {"rules": [
            {"enabled": True, "conditions": {"prefix": "secret-prefix"},
             "deleteObjectsTransition": {"condition": {"type": "Age", "maxAge": 7}}},
            {"enabled": False, "deleteObjectsTransition": {"condition": {"type": "Age", "maxAge": 1}}},
            {"enabled": True, "abortMultipartUploadsTransition": {"condition": {"maxAge": 1}}},
        ]}}
        summary = summarize_lifecycle(response)
        self.assertEqual(summary["enabled_rule_count"], 2)
        self.assertEqual(summary["enabled_object_deletion_rules"], 1)
        self.assertNotIn("secret-prefix", str(summary))
        self.assertFalse(summary["separate_media_backup_verified"])


if __name__ == "__main__":
    unittest.main()
