#!/usr/bin/env bash
set -euo pipefail

result_file="/etc/x-ui/install-result.env"
cloud_file="/etc/x-ui/stellagate-cloud.json"
activation_file="/etc/x-ui/stellagate-activation.json"

print_kv() {
  printf '%s=%s\n' "$1" "$2"
}

print_file_mode() {
  local path="$1"
  if [[ ! -e "$path" ]]; then
    print_kv "$2" "missing"
    return 0
  fi
  local mode
  mode="$(stat -c '%a' "$path" 2>/dev/null || stat -f '%Lp' "$path" 2>/dev/null || true)"
  print_kv "$2" "${mode:-unknown}"
}

print_kv "doctor" "stellagate"
print_kv "hostname" "$(hostname 2>/dev/null || true)"
print_kv "kernel" "$(uname -srmo 2>/dev/null || uname -a)"

if command -v systemctl >/dev/null 2>&1; then
  print_kv "x_ui_service" "$(systemctl is-active x-ui 2>/dev/null || true)"
else
  print_kv "x_ui_service" "systemctl_unavailable"
fi

print_file_mode "$result_file" "install_result_mode"
print_file_mode "$cloud_file" "cloud_config_mode"
print_file_mode "$activation_file" "activation_file_mode"

if [[ ! -r "$result_file" ]]; then
  print_kv "install_result" "unreadable"
  exit 0
fi

# The installer writes shell-escaped values with printf %q.
# shellcheck disable=SC1090
. "$result_file"

print_kv "panel_url" "${XUI_ACCESS_URL:-}"
print_kv "username" "${XUI_USERNAME:-}"
print_kv "password" "${XUI_PASSWORD:-}"
print_kv "db_type" "${XUI_DB_TYPE:-}"
print_kv "stellagate_panel" "${STELLAGATE_PANEL:-}"
print_kv "stellagate_template" "${STELLAGATE_TEMPLATE:-}"
print_kv "cloud_url" "${STELLAGATE_CLOUD_URL:-}"
print_kv "activation_required" "${STELLAGATE_ACTIVATION_REQUIRED:-false}"
print_kv "subscription_url" "${STELLAGATE_SUBSCRIPTION_URL:-}"
print_kv "api_token" "redacted"

if [[ -n "${XUI_PANEL_PORT:-}" && -n "${XUI_WEB_BASE_PATH:-}" && -n "${XUI_API_TOKEN:-}" ]]; then
  local_panel="http://127.0.0.1:${XUI_PANEL_PORT}/${XUI_WEB_BASE_PATH}"
  activation_status="$(curl -fsS --max-time 5 -H "Authorization: Bearer ${XUI_API_TOKEN}" "${local_panel}/panel/api/stella/activation/status" 2>/dev/null || true)"
  vps_status="$(curl -fsS --max-time 5 -H "Authorization: Bearer ${XUI_API_TOKEN}" "${local_panel}/panel/api/stella/vps/status" 2>/dev/null || true)"
  subscription_status="$(curl -fsS --max-time 5 -H "Authorization: Bearer ${XUI_API_TOKEN}" "${local_panel}/panel/api/stella/subscription" 2>/dev/null || true)"
  subscription_link="$(printf '%s' "$subscription_status" | sed -n 's/.*"link":"\([^"]*\)".*/\1/p')"
  print_kv "activation_status_json" "$activation_status"
  print_kv "vps_status_json" "$vps_status"
  print_kv "subscription_api_link" "$subscription_link"
fi
