# SignalRelay + DealLedger

**GTM automation becomes hard to trust when a seller cannot see why an account was prioritized or which sentence changed a deal field.**

This repository contains two headless, local-first GTM products:

- **SignalRelay** turns explicit fit, intent, timing, and data-confidence inputs into a traceable account priority and approval recommendation.
- **DealLedger** turns a discovery-call transcript into cited qualification evidence, missing-information flags, and a proposed CRM update.

Every recommendation preserves its inputs, evidence, confidence, proposed destination, and approval requirement. Python handles orchestration and connector contracts; C++ handles deterministic scoring and transcript evidence extraction. No external packages are required.
