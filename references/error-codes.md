# StellaGate Error Codes

Use these explanations in final replies. Keep them short and user-facing.

## Invite

| Code | Meaning | User-facing explanation |
| --- | --- | --- |
| `invite_invalid` | Invite is missing, malformed, or unknown | The invite code is invalid. Ask the Cloud admin for a fresh code. |
| `invite_expired` | Invite expired | The invite code has expired. Ask for a new code. |
| `invite_disabled` | Invite was disabled by admin | The invite code has been disabled. The Cloud admin must re-enable or replace it. |
| `invite_used_up` | Invite reached max uses | The invite code has already been used the allowed number of times. |
| `device_already_bound` | Same device already has an active activation | This VPS is already bound to an active StellaGate authorization. |
| `rate_limited` | Too many attempts | Too many activation attempts were made. Wait and retry. |

## Activation

| Code | Meaning | User-facing explanation |
| --- | --- | --- |
| `activation_invalid` | Activation state is invalid | The local activation state is invalid and should be reactivated. |
| `activation_revoked` | Authorization revoked | This VPS authorization was revoked in StellaGate-Cloud. |
| `activation_expired` | Authorization expired | This VPS authorization expired and must be renewed. |
| `token_invalid` | Activation token invalid | The saved activation token is invalid. Reactivation is required. |
| `token_missing` | Missing bearer token | The activation request is missing its token. |
| `invalid_token` | Current implementation equivalent of token invalid | The saved activation token is invalid. Reactivation is required. |
| `device_mismatch` | Token does not match device | The saved activation belongs to a different device. Reactivation is required. |
| `revoked` | Current implementation equivalent of revoked | This VPS authorization was revoked in StellaGate-Cloud. |
| `expired` | Current implementation equivalent of expired | This VPS authorization expired and must be renewed. |

## Cloud

| Code | Meaning | User-facing explanation |
| --- | --- | --- |
| `cloud_unreachable` | Network or DNS failure | The VPS cannot reach StellaGate-Cloud right now. Existing proxy service should keep running if it was already active. |
| `cloud_timeout` | Cloud did not respond in time | StellaGate-Cloud timed out. Retry after checking network and Cloud health. |
| `cloud_version_mismatch` | Unsupported API version | StellaGate-Cloud and StellaGate-UI are using incompatible API versions. |
| `cloud_not_configured` | No Cloud URL configured | StellaGate-UI does not have a Cloud address configured. |
| `invalid_cloud_url` | Cloud URL cannot be parsed | The Cloud URL is invalid. Use a full HTTPS URL. |
| `cloud_url_must_be_https` | Non-local HTTP Cloud URL | The Cloud URL must use HTTPS unless it is localhost development. |
| `cloud_http_400` | Cloud rejected request | The request was invalid. Check contract fields and local activation state. |
| `cloud_http_401` | Cloud rejected auth | The saved activation token is not accepted. Reactivation may be required. |
| `cloud_http_403` | Cloud rejected auth | The saved activation token is not authorized. Reactivation may be required. |
| `cloud_http_404` | Endpoint or activation not found | The Cloud endpoint or activation record was not found. |

## Local Install

| Code | Meaning | User-facing explanation |
| --- | --- | --- |
| `activation_save_failed` | Local activation file could not be written | The VPS could not save activation state. Check root permissions and `/etc/x-ui`. |
| `device_id_failed` | Device ID generation failed | The VPS could not generate a stable device ID. Check local system identity files and permissions. |
| `not_activated` | No local activation yet | StellaGate-UI is installed but still waiting for invite activation. |
