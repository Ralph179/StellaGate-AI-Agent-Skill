---
name: stellagate-ai-agent
description: Deploy, activate, inspect, and troubleshoot StellaGate-UI on a user's VPS through an AI agent workflow. Use when a user asks Codex, Claude Code, or another agent to install StellaGate-UI, configure StellaGate-Cloud, activate with an invite code, verify panel/Xray/subscription health, explain StellaGate activation errors, or check Cloud/UI API contract compatibility. Do not use for building a VPN marketplace, payment system, user registration, node selling, arbitrary remote shell, or storing VPS root credentials.
---

# StellaGate AI Agent

This skill helps an agent deploy StellaGate-UI on a user's VPS and verify that it is connected to StellaGate-Cloud. It is an operator workflow, not a consumer product backend.

## Non-Negotiable Boundaries

- Do not modify StellaGate-Cloud or StellaGate-UI unless the user explicitly asks for product code changes.
- Do not build an airport/proxy marketplace, payment, packages, node selling, registration, user center, or ticket system.
- Do not save VPS root passwords, SSH passwords, invite codes, API tokens, or activation tokens in files outside the target system's existing StellaGate paths.
- Do not expose or return `/etc/x-ui/stellagate-activation.json` contents or any `activation_token`.
- Do not provide an arbitrary remote shell interface. Run only narrow install, status, activation, and diagnostic commands needed for the user's request.
- Prefer HTTPS Cloud URLs. Localhost HTTP is only acceptable for local development.

## Resource Loading

Load only what the task needs:

- For install or post-install checks, read `references/deployment-runbook.md`.
- For Cloud/UI compatibility, API payloads, or contract drift, read `references/cloud-api-contract.md`.
- For error explanation or user-facing diagnosis, read `references/error-codes.md` or run `scripts/explain_error.py`.

## Deployment Workflow

1. Confirm the VPS target and access method from the user's provided context. If the user provided credentials directly, use the approved environment's normal SSH mechanism without persisting the password.
2. Inspect the VPS with read-only checks: OS, architecture, package manager, public IP, existing `x-ui`/StellaGate install, ports 80/443/2053/54321 as applicable, and service state.
3. Generate the installer command with `scripts/build_install_command.py`. Default Cloud URL is `https://stellagate.simuse.uk`.
4. Run the official StellaGate-UI installer only from the StellaGate-UI repository:
   `https://raw.githubusercontent.com/Ralph179/StellaGate-UI/codex/stellagate/install.sh`
5. If the user supplied an invite code, pass `--invite` to activate during install. If not, install with `--cloud` and report that activation must be completed in the local panel.
6. After install, run `scripts/stellagate_doctor.sh` on the VPS or mirror its checks manually. It reads existing root-only result files and redacts the local API token.
7. Verify:
   - `x-ui` systemd service is active or the equivalent service manager says it is running.
   - `/etc/x-ui/install-result.env` exists with mode `600`.
   - `/etc/x-ui/stellagate-cloud.json` contains the intended Cloud URL.
   - local activation status endpoint responds.
   - Xray status is running when activation and node creation completed.
   - subscription link exists after activation.
8. Return only the user-facing outputs: panel URL, username, password, subscription link if available, activation state, Xray state, and concise next steps.

## Commands

Build a safe install command:

```bash
python3 stellagate-ai-agent/scripts/build_install_command.py --cloud https://stellagate.simuse.uk
python3 stellagate-ai-agent/scripts/build_install_command.py --cloud https://stellagate.simuse.uk --invite SGC-XXXX-XXXX-XXXX
```

Explain an error:

```bash
python3 stellagate-ai-agent/scripts/explain_error.py invite_disabled
```

Run a read-only VPS doctor after install:

```bash
sudo bash stellagate-ai-agent/scripts/stellagate_doctor.sh
```

When the skill files are not present on the remote VPS, copy only the needed script or run equivalent commands manually. Do not upload unrelated repo contents.

## Final Response Shape

For successful deployments, include:

- Panel URL
- Username and password from `/etc/x-ui/install-result.env`
- Subscription link if present
- Activation state and Cloud URL
- Xray/service state

Never include `XUI_API_TOKEN`, `activation_token`, invite code values unless the user explicitly asks to repeat their own invite code, or raw contents of `/etc/x-ui/stellagate-activation.json`.

For failures, say exactly which stage failed: access, environment, installer download, service start, Cloud configuration, invite activation, node creation, subscription generation, or Xray health. Then map the StellaGate error code to plain language with `references/error-codes.md`.
