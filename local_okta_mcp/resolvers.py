"""
Resolves human-friendly identifiers to Okta IDs.

  Users  – accept  first.last  OR  first.last@domain  OR  full email
  Groups – accept  display name OR short/partial name
  Apps   – accept  display name OR partial name
"""

import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .client import OktaClient


def _org_domain() -> str | None:
    """Extract the email domain from the org URL if OKTA_ORG_DOMAIN is set,
    otherwise try to derive it from OKTA_CLIENT_ORGURL."""
    domain = os.environ.get("OKTA_ORG_DOMAIN", "").strip()
    if domain:
        return domain
    org_url = os.environ.get("OKTA_CLIENT_ORGURL", "")
    if org_url:
        # e.g. https://acme.okta.com  ->  acme.okta.com  (not useful as email domain)
        # Users should set OKTA_ORG_DOMAIN explicitly.
        pass
    return None


async def resolve_user(client: "OktaClient", login: str) -> dict:
    """
    Resolve *login* to an Okta user dict.

    Accepts:
      - Okta user ID (starts with "00o" / "00u" – passed through)
      - Full email:     john.smith@acme.com
      - Short login:    john.smith  (domain appended from OKTA_ORG_DOMAIN)
    """
    if login.startswith("00"):
        return await client.get_user(login)

    if "@" in login:
        return await client.get_user(login)

    domain = _org_domain()
    if domain:
        full = f"{login}@{domain}"
        try:
            return await client.get_user(full)
        except Exception:
            pass

    # Fall back: search by login prefix
    users = await client.list_users(q=login)
    exact = [u for u in users if u["profile"].get("login", "").lower().startswith(login.lower())]
    if len(exact) == 1:
        return exact[0]
    if len(exact) > 1:
        logins = [u["profile"]["login"] for u in exact]
        raise ValueError(
            f"Ambiguous user '{login}' – matches: {logins}. "
            "Provide a full email address."
        )
    raise ValueError(f"No Okta user found for '{login}'.")


async def resolve_group(client: "OktaClient", name: str) -> dict:
    """
    Resolve *name* to an Okta group dict.

    Accepts:
      - Okta group ID (starts with "00g") – passed through
      - Exact display name
      - Partial / short name  (case-insensitive prefix match)
    """
    if name.startswith("00"):
        return await client.get_group(name)

    groups = await client.list_groups(q=name)
    if not groups:
        raise ValueError(f"No Okta group found matching '{name}'.")

    # Prefer exact match
    exact = [g for g in groups if g["profile"]["name"].lower() == name.lower()]
    if len(exact) == 1:
        return exact[0]
    if len(exact) > 1:
        names = [g["profile"]["name"] for g in exact]
        raise ValueError(f"Multiple groups exactly match '{name}': {names}")

    if len(groups) == 1:
        return groups[0]

    names = [g["profile"]["name"] for g in groups]
    raise ValueError(
        f"Ambiguous group '{name}' – partial matches: {names}. "
        "Use a more specific name or the group ID."
    )


async def resolve_app(client: "OktaClient", name: str) -> dict:
    """
    Resolve *name* to an Okta application dict.

    Accepts:
      - Okta app ID – passed through
      - Exact label / name
      - Partial / short name  (case-insensitive prefix match)
    """
    # Okta app IDs start with "0oa"
    if name.startswith("0oa") or (len(name) == 20 and name.isalnum()):
        return await client.get_app(name)

    apps = await client.list_apps(q=name)
    if not apps:
        raise ValueError(f"No Okta application found matching '{name}'.")

    exact = [a for a in apps if a.get("label", "").lower() == name.lower()]
    if len(exact) == 1:
        return exact[0]
    if len(exact) > 1:
        labels = [a["label"] for a in exact]
        raise ValueError(f"Multiple apps exactly match '{name}': {labels}")

    if len(apps) == 1:
        return apps[0]

    labels = [a.get("label", a.get("name", "")) for a in apps]
    raise ValueError(
        f"Ambiguous app '{name}' – partial matches: {labels}. "
        "Use a more specific name or the app ID."
    )
