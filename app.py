#!/usr/bin/env python3
"""Mini SOC Lab web dashboard with live synthetic telemetry."""

from __future__ import annotations

from collections import Counter
from datetime import timedelta
from threading import Lock

from flask import Flask, jsonify, render_template, request

from detector import detect
from simulator import TelemetrySimulator

app = Flask(__name__)
SIM = TelemetrySimulator()
SIM.bootstrap(minutes=45, minimum_events=120)
SIM_LOCK = Lock()
MAX_EVENTS = 600


def serialize_event(event):
    return {
        "timestamp": event.timestamp.isoformat(timespec="seconds"),
        "source": event.source,
        "user": event.user,
        "action": event.action,
    }


def serialize_alert(alert):
    return {
        "timestamp": alert.timestamp.isoformat(timespec="seconds"),
        "source": alert.source,
        "user": alert.user,
        "rule": alert.rule,
        "severity": alert.severity,
        "message": alert.message,
    }


def snapshot(advance: bool = True):
    with SIM_LOCK:
        if advance:
            SIM.tick()
        events = SIM.events[-MAX_EVENTS:]
        alerts = detect(events)
        simulated_now = SIM.now

    severity = Counter(alert.severity for alert in alerts)
    actions = Counter(event.action for event in events)
    source_counts = Counter(event.source for event in events)
    user_counts = Counter(event.user for event in events)

    buckets = []
    for offset in range(11, -1, -1):
        minute = (simulated_now - timedelta(minutes=offset)).replace(second=0, microsecond=0)
        end = minute + timedelta(minutes=1)
        minute_events = [event for event in events if minute <= event.timestamp < end]
        buckets.append({
            "label": minute.strftime("%H:%M"),
            "count": len(minute_events),
            "failures": sum(event.action == "FAILURE" for event in minute_events),
        })

    return {
        "generated_at": simulated_now.isoformat(timespec="seconds"),
        "total_events": len(events),
        "failures": actions["FAILURE"],
        "successes": actions["SUCCESS"],
        "alert_count": len(alerts),
        "critical": severity["CRITICAL"],
        "high": severity["HIGH"],
        "medium": severity["MEDIUM"],
        "low": severity["LOW"],
        "unique_sources": len(source_counts),
        "top_sources": source_counts.most_common(6),
        "top_users": user_counts.most_common(6),
        "timeline": buckets,
        "alerts": [serialize_alert(alert) for alert in sorted(alerts, key=lambda item: item.timestamp, reverse=True)[:12]],
        "events": [serialize_event(event) for event in sorted(events, key=lambda item: item.timestamp, reverse=True)[:18]],
    }


@app.route("/")
def dashboard():
    return render_template("dashboard.html")


@app.route("/api/snapshot")
def api_snapshot():
    return jsonify(snapshot(advance=True))


@app.route("/api/reset", methods=["POST"])
def api_reset():
    with SIM_LOCK:
        SIM.bootstrap(minutes=45, minimum_events=120)
    return jsonify(snapshot(advance=False))


@app.route("/alerts")
def alerts_page():
    data = snapshot(advance=False)
    severity = request.args.get("severity", "ALL").upper()
    if severity != "ALL":
        data["alerts"] = [item for item in data["alerts"] if item["severity"] == severity]
    return render_template("alerts.html", **data, severity=severity)


@app.route("/events")
def events_page():
    data = snapshot(advance=False)
    query = request.args.get("q", "").strip().lower()
    if query:
        data["events"] = [
            event for event in data["events"]
            if query in event["source"].lower()
            or query in event["user"].lower()
            or query in event["action"].lower()
        ]
    return render_template("events.html", **data, query=query)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
