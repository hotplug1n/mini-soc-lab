# 🛡️ Mini SOC Lab

> Defensive security laboratory built with Python to simulate a small SOC workflow: **telemetry generation → collection → detection → triage → investigation**.

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Security](https://img.shields.io/badge/Security-Blue%20Team-0A66C2?style=for-the-badge&logo=shield&logoColor=white)](https://github.com/hotplug1n)
[![Flask](https://img.shields.io/badge/Flask-Web%20Dashboard-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)

## 🎯 Objective

Mini SOC Lab is a local defensive-security environment that turns synthetic authentication telemetry into structured detections and a live SOC-style dashboard.

The goal is to demonstrate practical concepts used in a junior Blue Team / SOC workflow without requiring a production SIEM.

## ⚙️ How it works

```text
Synthetic telemetry
       ↓
  event simulator
       ↓
 normalized events
       ↓
 detection engine
       ↓
 AUTH-001 / 002 / 003
       ↓
 live dashboard + triage
```

The simulator continuously produces varied authentication activity: normal logins, failures, privileged-account targeting, bursts of repeated failures and occasional successful logins after failed attempts.

All telemetry is synthetic. The dashboard explicitly represents a lab simulation, not a real corporate environment.

## 🚨 Detection scenarios

| Rule | Severity | Scenario |
|---|---|---|
| `AUTH-001` | HIGH | Repeated authentication failures from the same source against the same account |
| `AUTH-002` | CRITICAL | Successful authentication after a sequence of recent failures |
| `AUTH-003` | HIGH | Failed authentication targeting an administrative account |

## 🖥️ SOC dashboard

The web interface is designed as a clean enterprise-style monitoring console with:

- live synthetic event stream;
- rolling event-activity timeline;
- alert counters by severity;
- detection-rule activity;
- recent alerts with source, account, rule and timestamp;
- top source activity;
- normalized authentication event table;
- search and severity filters;
- simulation reset control.

The dashboard polls the local API every 3.5 seconds, so event counts and detections change without reloading the page.

## 🧠 Security concepts demonstrated

- Log parsing
- Event normalization
- Time-window correlation
- Detection engineering
- Alert severity
- Basic incident triage
- Python automation
- Synthetic telemetry generation
- Web dashboard design
- Unit testing
- Defensive security methodology

## 📂 Project structure

```text
mini-soc-lab/
├── README.md
├── app.py
├── detector.py
├── simulator.py
├── requirements.txt
├── data/
│   └── auth.log
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── alerts.html
│   └── events.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
├── tests/
│   └── test_detector.py
└── docs/
    ├── architecture.md
    ├── detection-rules.md
    └── investigation.md
```

## ▶️ Run the dashboard

Requires Python 3.10+.

```bash
python3 -m pip install -r requirements.txt
python3 app.py
```

Then open:

```text
http://127.0.0.1:5000
```

### CLI detector

The original detector remains available for direct log analysis:

```bash
python3 detector.py data/auth.log
```

### Tests

```bash
python3 -m unittest discover -s tests -v
```

## 🔍 Investigation workflow

When an alert appears, an analyst can validate the source address, affected account, failure count, timing, successful follow-on authentication and privileged-account targeting before deciding on containment or escalation.

The live simulator is intentionally probabilistic, so each run can produce a different mix of benign activity and suspicious patterns.

## 📊 Future improvements

- Windows Event Log / Sysmon support
- JSON alert export
- Sigma-compatible detection rules
- Splunk SPL examples
- IOC enrichment
- Configurable thresholds
- MITRE ATT&CK mapping
- CI test workflow
- Alert acknowledgement and case tracking
- Multiple telemetry sources (VPN, web, endpoint, DNS)

## 🔐 Scope and ethics

This repository is a **defensive laboratory project**. Use it only with data you own or environments where you have explicit authorization.

No real credentials, secrets or production telemetry should be committed to this repository.

## 👤 Author

**hotplug1n** — cybersecurity student focused on Blue Team, SOC, networking, Linux and secure software development.

[GitHub](https://github.com/hotplug1n) · [Studies](https://github.com/hotplug1n/studies) · [TryHackMe](https://tryhackme.com/p/.hotplug1n)
