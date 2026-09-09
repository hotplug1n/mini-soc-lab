import unittest
from datetime import datetime, timedelta

from detector import Event, detect, parse_event


class DetectorTests(unittest.TestCase):
    def test_parse_valid_event(self) -> None:
        event = parse_event("2026-09-08T14:00:01 192.0.2.50 user=admin action=FAILURE")
        self.assertIsNotNone(event)
        assert event is not None
        self.assertEqual(event.user, "admin")
        self.assertEqual(event.action, "FAILURE")

    def test_brute_force_detection(self) -> None:
        events = [
            Event(datetime(2026, 9, 8, 14, 0, i), "192.0.2.50", "user", "FAILURE")
            for i in range(1, 6)
        ]
        alerts = detect(events)
        self.assertTrue(any(alert.rule == "AUTH-001" for alert in alerts))

    def test_success_after_failures(self) -> None:
        events = [
            Event(datetime(2026, 9, 8, 14, 0, i), "192.0.2.50", "user", "FAILURE")
            for i in range(1, 4)
        ]
        events.append(Event(datetime(2026, 9, 8, 14, 0, 10), "192.0.2.50", "user", "SUCCESS"))
        alerts = detect(events)
        self.assertTrue(any(alert.rule == "AUTH-002" for alert in alerts))

    def test_admin_targeting(self) -> None:
        event = Event(datetime(2026, 9, 8, 14, 0, 1), "192.0.2.50", "admin", "FAILURE")
        alerts = detect([event])
        self.assertTrue(any(alert.rule == "AUTH-003" for alert in alerts))

    def test_old_failures_do_not_trigger_threshold(self) -> None:
        events = [
            Event(datetime(2026, 9, 8, 14, 0, 0) + timedelta(minutes=i), "192.0.2.50", "user", "FAILURE")
            for i in range(5)
        ]
        alerts = detect(events)
        self.assertFalse(any(alert.rule == "AUTH-001" for alert in alerts))


if __name__ == "__main__":
    unittest.main()
