# StellaGate AI Agent Skill

StellaGate AI Agent Skill is a deployment and troubleshooting skill for AI coding agents such as Codex and Claude Code. It helps an agent install StellaGate-UI on a user's VPS, connect it to StellaGate-Cloud, optionally activate it with an invite code, verify panel/Xray/subscription health, and explain common activation errors.

This repository is not StellaGate-Cloud and not StellaGate-UI. It is the agent-facing operation guide that keeps the deployment workflow consistent with both projects.

## What It Does

- Checks the VPS environment before installation
- Builds the official StellaGate-UI install command
- Configures the StellaGate-Cloud URL
- Optionally activates StellaGate-UI with an invite code
- Verifies panel, Xray, activation, and subscription status
- Explains StellaGate Cloud/UI error codes in plain language
- Protects sensitive values such as root passwords, local API tokens, and activation tokens

## What It Does Not Do

- Does not build an airport/proxy marketplace
- Does not add payment, packages, balance, orders, tickets, or user registration
- Does not sell nodes or manage shared traffic pools
- Does not store VPS root passwords or SSH passwords
- Does not expose arbitrary remote shell
- Does not print or persist `activation_token`

## Skill Layout

```text
.
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── cloud-api-contract.md
│   ├── deployment-runbook.md
│   └── error-codes.md
└── scripts/
    ├── build_install_command.py
    ├── explain_error.py
    └── stellagate_doctor.sh
```

## Quick Usage

Generate the default StellaGate-UI installer command:

```bash
python3 scripts/build_install_command.py --cloud https://stellagate.simuse.uk
```

Generate an installer command with invite activation:

```bash
python3 scripts/build_install_command.py --cloud https://stellagate.simuse.uk --invite SGC-XXXX-XXXX-XXXX
```

Explain an error code:

```bash
python3 scripts/explain_error.py invite_disabled
```

Run the read-only doctor script on an installed VPS:

```bash
sudo bash scripts/stellagate_doctor.sh
```

The doctor script redacts local API tokens and does not print activation tokens.

## Canonical Installer

The skill always uses the official StellaGate-UI installer:

```bash
curl -fsSL https://raw.githubusercontent.com/Ralph179/StellaGate-UI/codex/stellagate/install.sh | bash -s -- --cloud https://stellagate.simuse.uk
```

## Contract

The skill follows the shared StellaGate Cloud/UI API contract documented in:

- `references/cloud-api-contract.md`

If StellaGate-Cloud or StellaGate-UI contains a newer `docs/cloud-api-contract.md`, agents should load that file first and treat it as the current source of truth.
