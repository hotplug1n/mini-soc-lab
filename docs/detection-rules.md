# Detection Rules

## AUTH-001 — Brute Force

**Severity:** HIGH

Triggers when the same source and account reach five or more failed authentication attempts inside a five-minute window.

**Why it matters:** repeated failures can indicate password guessing or automated credential attacks.

**Initial triage:** inspect source, account, timing, authentication method and nearby events.

## AUTH-002 — Suspicious Success

**Severity:** CRITICAL

Triggers when a successful authentication occurs after at least three recent failures for the same source and account.

**Why it matters:** a successful login after repeated failures can indicate that a credential was eventually guessed or obtained.

**Initial triage:** validate whether the login was expected, review account activity and correlate surrounding telemetry.

## AUTH-003 — Administrative Account Targeting

**Severity:** HIGH

Triggers on failed authentication attempts against `admin`, `administrator` or `root`.

**Why it matters:** privileged accounts have greater potential impact if compromised.

**Initial triage:** verify whether the source is trusted, review the account's role and check for subsequent successful authentication.

## Detection engineering notes

These are intentionally simple baseline rules. In a production environment they would require tuning for normal authentication patterns, service accounts, VPN gateways, shared infrastructure and known administrative activity.
