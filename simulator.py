#!/usr/bin/env python3
"""Synthetic authentication telemetry generator for the Mini SOC Lab."""

from __future__ import annotations

import random
from datetime import datetime, timedelta

from detector import Event

USERS = ["alice", "bob", "carol", "dan", "analyst", "helpdesk", "admin", "administrator", "root"]
NORMAL_USERS = ["alice", "bob", "carol", "dan", "analyst", "helpdesk"]
PRIVATE_IPS = [f"10.20.{random.randint(1, 40)}.{random.randint(10, 240)}" for _ in range(24)]
LAB_EXTERNAL_IPS = [f"192.0.2.{n}" for n in range(20, 61)]
HOSTS = ["vpn-gateway", "jump-host", "web-01", "app-01", "db-01", "auth-01"]


class TelemetrySimulator:
    """Stateful, deterministic-in-shape synthetic SOC telemetry stream."""

    def __init__(self, seed: int | None = None) -> None:
        self.rng = random.Random(seed)
        self.now = datetime.now().replace(microsecond=0)
        self.events: list[Event] = []
        self.active_attack: dict[str, object] | None = None

    def _event(self, source: str, user: str, action: str, host: str | None = None) -> Event:
        event = Event(timestamp=self.now, source=source, user=user, action=action)
        return event

    def bootstrap(self, minutes: int = 45, minimum_events: int = 80) -> list[Event]:
        """Generate a realistic baseline with occasional attack sequences."""
        start = self.now - timedelta(minutes=minutes)
        self.events.clear()
        current = start
        target = max(minimum_events, minutes * 3)
        while len(self.events) < target:
            current += timedelta(seconds=self.rng.randint(3, 75))
            self.now = current
            self._emit_batch(max_events=3)

        self.now = datetime.now().replace(microsecond=0)
        return self.events[-600:]

    def tick(self) -> list[Event]:
        """Advance simulated time and emit 1-4 new events."""
        self.now += timedelta(seconds=self.rng.randint(2, 15))
        count = self.rng.choices([1, 2, 3, 4], weights=[45, 35, 15, 5], k=1)[0]
        return self._emit_batch(count)

    def _emit_batch(self, max_events: int) -> list[Event]:
        new_events: list[Event] = []

        if self.active_attack:
            new_events.extend(self._emit_attack())
            if not self.active_attack:
                new_events.extend(self._normal_events(max_events))
        else:
            new_events.extend(self._normal_events(max_events))
            if self.rng.random() < 0.055:
                self._start_attack()

        self.events.extend(new_events)
        self.events = self.events[-600:]
        return new_events

    def _normal_events(self, max_events: int) -> list[Event]:
        out: list[Event] = []
        for _ in range(max_events):
            source = self.rng.choice(PRIVATE_IPS + LAB_EXTERNAL_IPS)
            user = self.rng.choice(NORMAL_USERS)
            action = "SUCCESS" if self.rng.random() < 0.92 else "FAILURE"
            if self.rng.random() < 0.035:
                user = self.rng.choice(["admin", "administrator", "root"])
                action = "FAILURE"
            out.append(self._event(source, user, action))
            self.now += timedelta(seconds=self.rng.randint(1, 9))
        return out

    def _start_attack(self) -> None:
        source = self.rng.choice(LAB_EXTERNAL_IPS)
        user = self.rng.choice(["admin", "administrator", "root", "analyst"])
        self.active_attack = {"source": source, "user": user, "remaining": self.rng.randint(4, 8), "successful": False}

    def _emit_attack(self) -> list[Event]:
        if not self.active_attack:
            return []
        source = str(self.active_attack["source"])
        user = str(self.active_attack["user"])
        remaining = int(self.active_attack["remaining"])
        out: list[Event] = []

        if remaining > 1:
            burst = min(self.rng.randint(1, 3), remaining - 1)
            for _ in range(burst):
                out.append(self._event(source, user, "FAILURE"))
                self.now += timedelta(seconds=self.rng.randint(2, 12))
                remaining -= 1
            self.active_attack["remaining"] = remaining
            return out

        success = self.rng.random() < 0.42
        if success:
            out.append(self._event(source, user, "SUCCESS"))
        else:
            out.append(self._event(source, user, "FAILURE"))
        self.active_attack = None
        return out
