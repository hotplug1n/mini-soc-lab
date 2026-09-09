# Architecture

## Data flow

```text
Synthetic authentication logs
            |
            v
      log parser (Python)
            |
            v
      normalized events
            |
            v
     detection engine
       /      |      \
      v       v       v
 AUTH-001  AUTH-002  AUTH-003
      \       |       /
       \      |      /
        v     v     v
          triage report
```

## Components

### Log source

`data/auth.log` contains synthetic authentication events designed for repeatable testing. No production telemetry is used.

### Parser

`detector.py` validates each line and converts supported records into an `Event` object containing timestamp, source, username and action.

### Detection engine

Events are correlated by `(source, user)` within a five-minute sliding window. The engine emits structured `Alert` objects with rule ID, severity and context.

### Output

The command-line report sorts alerts by severity and timestamp so an analyst can triage the highest-impact events first.

## Design goals

- deterministic results;
- small attack-surface and zero third-party dependencies;
- readable detection logic;
- testable components;
- easy future integration with SIEM data.
