#!/usr/bin/env python3
"""Explain StellaGate authorization and local panel error codes."""

from __future__ import annotations

import argparse


EXPLANATIONS = {
    "invite_invalid": "The invite code is invalid. Ask the author/admin for a fresh code.",
    "invite_expired": "The invite code has expired. Ask for a new code.",
    "invite_disabled": "The invite code has been disabled. The author/admin must re-enable or replace it.",
    "invite_used_up": "The invite code has already been used the allowed number of times.",
    "device_already_bound": "This VPS is already bound to an active StellaGate authorization.",
    "rate_limited": "Too many activation attempts were made. Wait and retry.",
    "activation_invalid": "The local activation state is invalid and should be reactivated.",
    "activation_revoked": "This VPS authorization was revoked by the author/admin.",
    "activation_expired": "This VPS authorization expired and must be renewed.",
    "token_invalid": "The saved activation token is invalid. Reactivation is required.",
    "token_missing": "The activation request is missing its token.",
    "invalid_token": "The saved activation token is invalid. Reactivation is required.",
    "device_mismatch": "The saved activation belongs to a different device. Reactivation is required.",
    "revoked": "This VPS authorization was revoked by the author/admin.",
    "expired": "This VPS authorization expired and must be renewed.",
    "cloud_unreachable": "The VPS cannot reach the authorization endpoint right now.",
    "cloud_timeout": "The authorization endpoint timed out. Retry after checking network health.",
    "cloud_version_mismatch": "The authorization endpoint and StellaGate-UI are using incompatible API versions.",
    "cloud_not_configured": "StellaGate-UI does not have an authorization endpoint address configured.",
    "invalid_cloud_url": "The authorization endpoint URL is invalid. Use a full HTTPS URL.",
    "cloud_url_must_be_https": "The authorization endpoint URL must use HTTPS unless it is localhost development.",
    "activation_save_failed": "The VPS could not save activation state. Check root permissions and /etc/x-ui.",
    "device_id_failed": "The VPS could not generate a stable device ID.",
    "not_activated": "StellaGate-UI is installed but still waiting for invite activation.",
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Explain StellaGate error codes.")
    parser.add_argument("code", nargs="+", help="One or more error codes")
    args = parser.parse_args()

    for code in args.code:
        normalized = code.strip()
        print(f"{normalized}: {EXPLANATIONS.get(normalized, 'Unknown StellaGate error. Check authorization API logs and contract drift.')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
