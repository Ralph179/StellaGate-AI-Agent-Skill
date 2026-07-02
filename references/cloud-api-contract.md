# StellaGate Authorization API Contract

This is the authorization contract the StellaGate AI Agent must expect when deploying or checking StellaGate-UI. If the target repositories contain a newer contract document, load that file first and treat it as the current source of truth. Use this reference as the baseline contract and drift checklist.

## Scope

The author-side management system is private. StellaGate-UI is the user-facing local VPS panel. The AI Agent only installs, activates, checks, and explains; it does not replace the product UI.

## Versioning

API v1 uses version headers defined by the current implementation and this request body field:

Every request body should include:

```json
{ "api_version": 1 }
```

Every authorization service response should include:

```json
{ "api_version": 1, "success": true }
```

If version negotiation is unsupported in the checked implementation, report it as contract drift rather than silently inventing behavior.

## Naming

Use `snake_case` for wire fields. Required names include:

- `invite_code`
- `device_id`
- `server_id`
- `activation_token`
- `public_ip`
- `panel_version`
- `agent_version`
- `current_protocol`
- `current_port`
- `xray_status`
- `cpu_pct`
- `mem_pct`
- `disk_pct`

## Claim

`POST /api/activation/claim`

Called by StellaGate-UI after a user submits an invite code, or indirectly when the installer activates through the local UI endpoint.

Request:

```json
{
  "api_version": 1,
  "invite_code": "SGC-XXXX-XXXX-XXXX",
  "device_id": "...",
  "hostname": "...",
  "public_ip": "...",
  "os": "...",
  "arch": "...",
  "panel_version": "...",
  "agent_version": "..."
}
```

Success:

```json
{
  "api_version": 1,
  "success": true,
  "server_id": "srv_xxx",
  "activation_token": "SGA_xxx"
}
```

Failure:

```json
{
  "api_version": 1,
  "success": false,
  "error": "invite_invalid",
  "message": "Invalid invite code"
}
```

## Check

`POST /api/activation/check`

Header:

```http
Authorization: Bearer ACTIVATION_TOKEN
```

Request:

```json
{
  "api_version": 1,
  "server_id": "srv_xxx",
  "device_id": "...",
  "panel_version": "...",
  "public_ip": "..."
}
```

Active:

```json
{
  "api_version": 1,
  "success": true,
  "active": true,
  "server_id": "srv_xxx",
  "message": "activated"
}
```

Revoked:

```json
{
  "api_version": 1,
  "success": true,
  "active": false,
  "reason": "revoked"
}
```

## Heartbeat

`POST /api/activation/heartbeat`

Header:

```http
Authorization: Bearer ACTIVATION_TOKEN
```

Request:

```json
{
  "api_version": 1,
  "server_id": "srv_xxx",
  "device_id": "...",
  "hostname": "...",
  "public_ip": "...",
  "os": "...",
  "arch": "...",
  "cpu_pct": 12.5,
  "mem_pct": 43.2,
  "disk_pct": 61.7,
  "xray_status": "running",
  "current_protocol": "vless-reality",
  "current_port": 443,
  "upload": 123456,
  "download": 654321,
  "panel_version": "...",
  "agent_version": "..."
}
```

Success:

```json
{
  "api_version": 1,
  "success": true,
  "active": true
}
```

Revoked:

```json
{
  "api_version": 1,
  "success": false,
  "active": false,
  "reason": "revoked"
}
```

## Token And Device Rules

- The authorization service returns plaintext `activation_token` only once.
- The authorization service stores only the activation token hash and device ID hash.
- StellaGate-UI stores plaintext `activation_token` only in `/etc/x-ui/stellagate-activation.json` with mode `0600`.
- The Agent must not print, copy, cache, or persist `activation_token`.
- `device_id` must be stable for the VPS and should be generated from machine identity plus a local random secret.

## Online State

StellaGate-UI sends heartbeat every 60 seconds. The authorization service treats `last_seen_at < 90s` as `online`; older heartbeats are `offline`. Revoked activations should display `revoked`. Temporary authorization service network failures should not stop local Xray; explicit invalidation should lock the panel and disable the managed node.
