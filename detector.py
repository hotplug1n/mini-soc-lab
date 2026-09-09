#!/usr/bin/env python3
"""Mini SOC Lab: defensive authentication log detector."""

from __future__ import annotations

import argparse
import re
from collections import defaultdict, deque
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path

LOG_PATTERN = re.compile(
    r"^(?P<timestamp>\S+T\S+)\s+(?P<source>\S+)\s+"
    r"user=(?P<user>\S+)\s+action=(?P<action>SUCCESS|FAILURE)$"
)

FAILURE_THRESHOLD = 5
FAILURE_WINDOW = timedelta(minutes=5)
ADMIN_ACCOUNTS = {"admin", "administrator", "root"}


@dataclass(frozen=True)
class Event:
    timestamp: datetime
    source: str
    user: str
    action: str


@dataclass(frozen=True)
class Alert:
    rule: str
    severity: str
    source: str
    user: str
    message: str
    timestamp: datetime


def parse_event(line: str, line_number: int = 0) -> Event | None:
    match = LOG_PATTERN.match(line.strip())
    if not match:
        return None

    try:
        timestamp = datetime.fromisoformat(match.group("timestamp"))
    except ValueError:
        return None

    return Event(
        timestamp=timestamp,
        source=match.group("source"),
        user=match.group("user"),
        action=match.group("action"),
    )


def detect(events: list[Event]) -> list[Alert]:
    alerts: list[Alert] = []
    failures: dict[tuple[str, str], deque[Event]] = defaultdict(deque)

    for event in sorted(events, key=lambda item: item.timestamp):
        key = (event.source, event.user)
        queue = failures[key]

        if event.action == "FAILURE":
            queue.append(event)
            cutoff = event.timestamp - FAILURE_WINDOW
            while queue and queue[0].timestamp < cutoff:
                queue.popleft()

            if len(queue) == FAILURE_THRESHOLD:
                alerts.append(Alert(
                    rule="AUTH-001",
                    severity="HIGH",
                    source=event.source,
                    user=event.user,
                    message=f"{len(queue)} failed authentication attempts within 5 minutes",
                    timestamp=event.timestamp,
                ))

            if event.user.lower() in ADMIN_ACCOUNTS:
                alerts.append(Alert(
                    rule="AUTH-003",
                    severity="HIGH",
                    source=event.source,
                    user=event.user,
                    message="administrative account targeted",
                    timestamp=event.timestamp,
                ))

        elif event.action == "SUCCESS":
            recent = [e for e in queue if event.timestamp - e.timestamp <= FAILURE_WINDOW]
            if len(recent) >= 3:
                alerts.append(Alert(
                    rule="AUTH-002",
                    severity="CRITICAL",
                    source=event.source,
                    user=event.user,
                    message=f"successful login after {len(recent)} recent failures",
                    timestamp=event.timestamp,
                ))
            queue.clear()

    return alerts


def load_events(path: Path) -> tuple[list[Event], int]:
    events: list[Event] = []
    malformed = 0
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        event = parse_event(line, line_number)
        if event is None:
            malformed += 1
            continue
        events.append(event)
    return events, malformed


def print_report(events: list[Event], alerts: list[Alert], malformed: int) -> None:
    severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    print("=== Mini SOC Lab ===")
    print(f"Events analyzed : {len(events)}")
    print(f"Malformed lines : {malformed}")
    print(f"Alerts generated: {len(alerts)}")
    print()

    if not alerts:
        print("No suspicious authentication patterns detected.")
        return

    for alert in sorted(alerts, key=lambda item: (severity_order.get(item.severity, 9), item.timestamp)):
        print(
            f"[{alert.severity}] {alert.rule} {alert.source} -> {alert.user} | "
            f"{alert.message} | {alert.timestamp.isoformat()}"
        )


def main() -> int:
    parser = argparse.ArgumentParser(description="Detect suspicious authentication patterns in lab logs.")
    parser.add_argument("logfile", type=Path, help="path to authentication log")
    args = parser.parse_args()

    if not args.logfile.is_file():
        parser.error(f"log file not found: {args.logfile}")

    events, malformed = load_events(args.logfile)
    print_report(events, detect(events), malformed)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
