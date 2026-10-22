# SignalRelay + DealLedger

**GTM automation becomes hard to trust when a seller cannot see why an account was prioritized or which sentence changed a deal field.**

This repository contains two headless, local-first GTM products:

- **SignalRelay** turns explicit fit, intent, timing, and data-confidence inputs into a traceable account priority and approval recommendation.
- **DealLedger** turns a discovery-call transcript into cited qualification evidence, missing-information flags, and a proposed CRM update.

Every recommendation preserves its inputs, evidence, confidence, proposed destination, and approval requirement. Python handles orchestration and connector contracts; C++ handles deterministic scoring and transcript evidence extraction. No external packages are required.

## Run SignalRelay

```bash
make
python3 python/app.py score --account "Acme" --fit 88 --intent 72 --timing 60 --confidence 95
```

## Run DealLedger

```bash
python3 python/app.py analyze --deal "Acme renewal" --transcript-file examples/discovery.txt
```

## Test

```bash
make test
```

## Connector boundary

The demo does not pretend to contact live customer systems. `python/connectors.py` documents the intended production connections:

| Product | Read from | Write to | Approval gate |
|---|---|---|---|
| SignalRelay | Apollo/Clay + HubSpot | Apollo sequence + HubSpot note | Required before enrichment spend, enrollment, or send |
| DealLedger | Gong/Zoom/Meet + HubSpot | HubSpot fields, note, and task | Required before every CRM write |

Replace the mock adapters with scoped MCP clients or vendor APIs. Keep deduplication, scoring, field mapping, and writes deterministic and auditable.

All inputs and outputs are demonstrations. The repository contains no customer data, claimed revenue impact, or live outbound automation.
