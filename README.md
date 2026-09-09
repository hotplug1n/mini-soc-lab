# 🛡️ Mini SOC Lab

> Defensive security laboratory built with Python to simulate a small SOC workflow: **log collection → detection → triage → investigation → response recommendations**.

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Security](https://img.shields.io/badge/Security-Blue%20Team-0A66C2?style=for-the-badge&logo=shield&logoColor=white)](https://github.com/hotplug1n)
[![Flask](https://img.shields.io/badge/Flask-Web%20Dashboard-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)

## 🎯 Objective

This project demonstrates how a junior security analyst can turn authentication logs into actionable alerts and inspect them through a lightweight SOC-style web dashboard.

The lab focuses on reproducible detection logic rather than offensive exploitation.

### Detection scenarios

| Rule | Severity | Scenario |
|---|---|---|
| `AUTH-001` | HIGH | Repeated authentication failures from the same source against the same account |
| `AUTH-002` | CRITICAL | Successful authentication after a sequence of recent failures |
| `AUTH-003` | HIGH | Failed authentication targeting an administrative account |

## 🧠 Security concepts demonstrated

- Log parsing
- Event normalization
- Time-window correlation
- Detection engineering
- Alert severity
- Basic incident triage
- Python automation
- Unit testing
- SOC dashboard design
- Defensive security methodology

## 🖥️ Web dashboard

The project includes a local Flask interface with:

- Security overview and metrics
- Critical / High / Medium / Low alert counts
- Latest detections
- Alert filtering by severity
- Event search by IP, user or action
- Detection-engine status indicator
- Source activity overview

## 🏗️ Architecture

```text
                    ┌──────────────────┐
                    │   auth.log       │
                    │  lab telemetry   │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │   Log Parser     │
                    │     Python       │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Detection Engine │
                    │  AUTH-001..003   │
                    └────────┬─────────┘
                             │
                  ┌──────────┴──────────┐
                  ▼                     ▼
         ┌─────────────────┐   ┌─────────────────┐
         │ CLI report      │   │ Flask dashboard │
         │ terminal output │   │ alerts / events│
         └─────────────────┘   └─────────────────┘
```

## 📂 Project structure

```text
mini-soc-lab/
├── README.md
├── app.py
├── detector.py
├── requirements.txt
├── data/
│   └── auth.log
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── alerts.html
│   └── events.html
├── static/
│   └── css/
│       └── style.css
├── tests/
│   └── test_detector.py
└── docs/
    ├── architecture.md
    ├── detection-rules.md
    └── investigation.md
```

## ▶️ Run the detector

Requires Python 3.10+.

```bash
python3 detector.py data/auth.log
```

## 🖥️ Run the dashboard

Install the single web dependency:

```bash
python3 -m pip install -r requirements.txt
```

Start the local server:

```bash
python3 app.py
```

Then open:

```text
http://127.0.0.1:5000
```

The dashboard reads the synthetic `data/auth.log` file and runs the same detection engine used by the CLI.

## 🧪 Run tests

```bash
python3 -m unittest discover -s tests -v
```

## 🔍 Investigation workflow

When an alert is generated, the analyst should validate:

1. Source address and affected account.
2. Number and timing of failed attempts.
3. Whether a successful login followed the failures.
4. Whether the targeted account has administrative privileges.
5. Related events in the surrounding time window.
6. Appropriate containment, credential-reset, monitoring and escalation actions.

The repository contains synthetic lab telemetry only. Addresses in the sample data use documentation ranges.

## 📊 Future improvements

- Windows Event Log / Sysmon support
- JSON alert export
- Sigma-compatible detection rules
- Splunk SPL examples
- IOC enrichment
- Configurable thresholds
- MITRE ATT&CK mapping
- CI test workflow

## 🔐 Scope and ethics

This repository is a **defensive laboratory project**. Use it only with data you own or environments where you have explicit authorization.

No real credentials, secrets, or production telemetry should be committed to this repository.

## 👤 Author

**hotplug1n** — cybersecurity student focused on Blue Team, SOC, networking, Linux and secure software development.

[GitHub](https://github.com/hotplug1n) · [Studies](https://github.com/hotplug1n/studies) · [TryHackMe](https://tryhackme.com/p/.hotplug1n)
