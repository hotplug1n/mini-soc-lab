#!/usr/bin/env python3
"""Mini SOC Lab web dashboard."""

from __future__ import annotations

from pathlib import Path
from flask import Flask, render_template, request

from detector import detect, load_events

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_LOG = BASE_DIR / "data" / "auth.log"

app = Flask(__name__)


def dashboard_data(log_path: Path):
    events, malformed = load_events(log_path)
    alerts = detect(events)

    severity_counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
    rule_counts = {}
    source_counts = {}
    user_counts = {}
    failures = successes = 0

    for event in events:
        if event.action == "FAILURE":
            failures += 1
        else:
            successes += 1
        source_counts[event.source] = source_counts.get(event.source, 0) + 1
        user_counts[event.user] = user_counts.get(event.user, 0) + 1

    for alert in alerts:
        severity_counts[alert.severity] = severity_counts.get(alert.severity, 0) + 1
        rule_counts[alert.rule] = rule_counts.get(alert.rule, 0) + 1

    recent = sorted(alerts, key=lambda alert: alert.timestamp, reverse=True)[:12]
    top_sources = sorted(source_counts.items(), key=lambda item: item[1], reverse=True)[:8]
    top_users = sorted(user_counts.items(), key=lambda item: item[1], reverse=True)[:8]

    return {
        "events": events,
        "alerts": alerts,
        "recent": recent,
        "malformed": malformed,
        "total_events": len(events),
        "failures": failures,
        "successes": successes,
        "severity_counts": severity_counts,
        "rule_counts": rule_counts,
        "top_sources": top_sources,
        "top_users": top_users,
        "log_name": log_path.name,
    }


@app.route("/")
def dashboard():
    query = request.args.get("q", "").strip().lower()
    data = dashboard_data(DEFAULT_LOG)

    if query:
        data["recent"] = [
            alert for alert in data["alerts"]
            if query in alert.source.lower()
            or query in alert.user.lower()
            or query in alert.rule.lower()
            or query in alert.message.lower()
        ][:12]

    return render_template("dashboard.html", **data, query=query)


@app.route("/alerts")
def alerts_page():
    data = dashboard_data(DEFAULT_LOG)
    severity = request.args.get("severity", "ALL").upper()
    filtered = data["alerts"]
    if severity != "ALL":
        filtered = [alert for alert in filtered if alert.severity == severity]
    data["alerts"] = sorted(filtered, key=lambda alert: alert.timestamp, reverse=True)
    return render_template("alerts.html", **data, severity=severity)


@app.route("/events")
def events_page():
    data = dashboard_data(DEFAULT_LOG)
    query = request.args.get("q", "").strip().lower()
    filtered = data["events"]
    if query:
        filtered = [
            event for event in filtered
            if query in event.source.lower()
            or query in event.user.lower()
            or query in event.action.lower()
        ]
    data["events"] = sorted(filtered, key=lambda event: event.timestamp, reverse=True)
    return render_template("events.html", **data, query=query)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
