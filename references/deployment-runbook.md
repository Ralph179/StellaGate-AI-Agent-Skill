# StellaGate AI Agent Deployment Runbook

## Inputs

Collect only what is necessary:

- VPS host/IP and SSH user/access method
- Cloud URL, defaulting to `https://stellagate.simuse.uk`
- Optional invite code
- Optional desired protocol only if the current installer supports it; otherwise the panel can switch protocols after activation

Do not store VPS passwords, SSH private keys, invite codes, `XUI_API_TOKEN`, or activation tokens in new files.

## Preflight

Run read-only checks first:

```bash
uname -a
id
command -v curl || true
command -v systemctl || true
ss -ltnp 2>/dev/null | sed -n '1,80p' || true
test -f /etc/x-ui/install-result.env && ls -l /etc/x-ui/install-result.env || true
systemctl is-active x-ui 2>/dev/null || true
```

If an existing StellaGate-UI install is found, ask before reinstalling or overwriting. A normal health check may proceed without asking.

## Install

Generate the command locally:

```bash
python3 stellagate-ai-agent/scripts/build_install_command.py --cloud https://stellagate.simuse.uk
```

With invite activation:

```bash
python3 stellagate-ai-agent/scripts/build_install_command.py --cloud https://stellagate.simuse.uk --invite SGC-XXXX-XXXX-XXXX
```

The canonical installer source is:

```text
https://raw.githubusercontent.com/Ralph179/StellaGate-UI/codex/stellagate/install.sh
```

The installer writes:

- `/etc/x-ui/install-result.env` with `XUI_ACCESS_URL`, `XUI_USERNAME`, `XUI_PASSWORD`, `XUI_API_TOKEN`, and StellaGate result fields
- `/etc/x-ui/stellagate-cloud.json` with `cloud_url`
- `/etc/x-ui/stellagate-activation.json` only after successful activation

## Post-Install Checks

Use the bundled doctor script on the VPS when possible:

```bash
sudo bash stellagate-ai-agent/scripts/stellagate_doctor.sh
```

Manual equivalent:

```bash
sudo test -f /etc/x-ui/install-result.env
sudo stat -c '%a %n' /etc/x-ui/install-result.env 2>/dev/null || sudo stat -f '%Lp %N' /etc/x-ui/install-result.env
sudo systemctl is-active x-ui
sudo bash -lc '. /etc/x-ui/install-result.env; printf "%s\n" "$XUI_ACCESS_URL"'
```

If activation was supplied, also verify:

```bash
sudo test -f /etc/x-ui/stellagate-activation.json
sudo stat -c '%a %n' /etc/x-ui/stellagate-activation.json 2>/dev/null || sudo stat -f '%Lp %N' /etc/x-ui/stellagate-activation.json
```

Do not print `XUI_API_TOKEN` or any field from `stellagate-activation.json`.

## Local API Checks

Source `install-result.env` inside the remote shell and use `XUI_API_TOKEN` only as a request header:

```bash
. /etc/x-ui/install-result.env
local_panel="http://127.0.0.1:${XUI_PANEL_PORT}/${XUI_WEB_BASE_PATH}"
curl -fsS -H "Authorization: Bearer ${XUI_API_TOKEN}" "${local_panel}/panel/api/stella/activation/status"
curl -fsS -H "Authorization: Bearer ${XUI_API_TOKEN}" "${local_panel}/panel/api/stella/vps/status"
curl -fsS -H "Authorization: Bearer ${XUI_API_TOKEN}" "${local_panel}/panel/api/stella/subscription"
```

Only report safe response fields. The subscription endpoint may include both `link` and a bare `token`; return the subscription `link` only and redact the bare token.

## Final Report

Return:

- Panel URL
- Username
- Password
- Subscription link if available
- Cloud URL
- Activation state
- Xray/service state

Also include what was not completed, such as "invite not provided, activation is waiting in the panel" or "Cloud returned `invite_disabled`, so the panel installed but is still locked."
