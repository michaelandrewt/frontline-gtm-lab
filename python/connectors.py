"""Production connector contracts; demo adapters never call external systems."""

CONNECTORS = {
    "signal_relay": {
        "reads": ["Apollo or Clay: people, accounts, enrichment, signals", "HubSpot: ownership, lifecycle, activity, suppression"],
        "proposes": ["Apollo: list and sequence enrollment", "HubSpot: score explanation and activity note"],
        "guardrails": ["human approval before paid enrichment", "human approval before enrollment or send", "source URL and timestamp required"],
    },
    "deal_ledger": {
        "reads": ["Gong: synthesized deal insight", "Zoom or Meet: meeting artifacts", "HubSpot: deal and activity context"],
        "proposes": ["HubSpot: qualification fields", "HubSpot: note and follow-up task"],
        "guardrails": ["human approval before CRM write", "verbatim evidence for every populated field", "missing evidence stays missing"],
    },
}


def public_contract():
    return CONNECTORS

