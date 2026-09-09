# Architecture

## Live data flow

```text
          synthetic telemetry simulator
                     |
                     v
              normalized Event
                     |
                     v
              detection engine
              /       |       \
             v        v        v
         AUTH-001  AUTH-002  AUTH-003
             \        |        /
              \       |       /
               v      v      v
                 Flask API
                     |
                     v
              SOC web dashboard
```

## Components

### Telemetry simulator

`simulator.py` generates synthetic authentication events with randomized source addresses, users, actions and attack-like sequences. It keeps a bounded in-memory stream so the dashboard behaves like a small live monitoring console without requiring real infrastructure.

The simulator intentionally produces a mixture of benign activity and suspicious patterns. This makes the UI non-static while keeping the project safe and reproducible as a laboratory exercise.

### Detection engine

`detector.py` validates event records and correlates failures by `(source, user)` using a five-minute sliding window. It emits structured `Alert` objects for the three baseline authentication rules.

### Flask API

`app.py` keeps the simulated event stream in memory and exposes `/api/snapshot` for the dashboard. Each snapshot advances the simulation and recalculates detections from the retained events. `/api/reset` starts a fresh simulated session.

### Dashboard

The browser uses lightweight vanilla JavaScript to poll the local API every 3.5 seconds. No external frontend framework is required. The interface displays event activity, detection counts, top sources, current alerts and recent normalized events.

## Data retention

The application retains the most recent 600 synthetic events in memory. No production telemetry is written or transmitted by the dashboard.

## Design goals

- realistic-looking but clearly synthetic telemetry;
- deterministic detection logic;
- bounded memory usage;
- minimal dependencies;
- readable code and testable detection components;
- architecture that can later accept SIEM or endpoint telemetry.
