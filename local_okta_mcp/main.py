#!/usr/bin/env python3
"""
Okta MCP Server – FastMCP 2.0
Exposes the full Okta management API surface as MCP tools.

Start:
    python local_okta_mcp/main.py

Requires .env (run  python local_okta_mcp/setup.py  first):
    OKTA_CLIENT_ORGURL=https://acme.okta.com
    OKTA_API_TOKEN=...
    OKTA_ORG_DOMAIN=acme.com          # optional, enables  first.last  shortnames
"""

from __future__ import annotations

import os
from typing import Any

from dotenv import load_dotenv
from fastmcp import FastMCP

load_dotenv()

from .client import OktaClient  # noqa: E402
from .resolvers import resolve_app, resolve_group, resolve_user  # noqa: E402

mcp = FastMCP("Okta MCP", version="2.1.0")


def _client() -> OktaClient:
    return OktaClient()


# =========================================================================
# USER MANAGEMENT
# =========================================================================


@mcp.tool()
async def list_users(
    query: str = "",
    search: str = "",
    filter_expr: str = "",
) -> list[dict]:
    """
    List / search Okta users.

    Provide at most one of:
      query       – simple string search across login, name, email
      search      – Okta SCIM filter expression, e.g. 'status eq "ACTIVE"'
      filter_expr – legacy Okta filter expression
    """
    return await _client().list_users(
        q=query or None,
        search=search or None,
        filter_=filter_expr or None,
    )


@mcp.tool()
async def get_user(login: str) -> dict:
    """
    Get an Okta user's full profile.

    *login* accepts:
      - first.last          (OKTA_ORG_DOMAIN must be set for shortname resolution)
      - first.last@acme.com
      - Okta user ID
    """
    return await resolve_user(_client(), login)


@mcp.tool()
async def create_user(
    first_name: str,
    last_name: str,
    email: str,
    login: str = "",
    mobile_phone: str = "",
    activate: bool = True,
    temp_password: str = "",
) -> dict:
    """
    Create a new Okta user.

    *login* defaults to *email* if omitted.
    Set *activate=False* to create in STAGED status.
    Provide *temp_password* to set an initial password (skip activation email).
    """
    profile: dict[str, Any] = {
        "firstName": first_name,
        "lastName": last_name,
        "email": email,
        "login": login or email,
    }
    if mobile_phone:
        profile["mobilePhone"] = mobile_phone

    credentials: dict | None = None
    if temp_password:
        credentials = {"password": {"value": temp_password}}

    return await _client().create_user(profile, credentials, activate)


@mcp.tool()
async def update_user(
    login: str,
    first_name: str = "",
    last_name: str = "",
    email: str = "",
    mobile_phone: str = "",
    title: str = "",
    department: str = "",
    manager: str = "",
    organization: str = "",
) -> dict:
    """
    Update profile fields for an existing Okta user.

    *login* accepts first.last, full email, or Okta user ID.
    Only non-empty fields are changed.
    """
    profile: dict[str, Any] = {}
    if first_name:
        profile["firstName"] = first_name
    if last_name:
        profile["lastName"] = last_name
    if email:
        profile["email"] = email
    if mobile_phone:
        profile["mobilePhone"] = mobile_phone
    if title:
        profile["title"] = title
    if department:
        profile["department"] = department
    if manager:
        profile["manager"] = manager
    if organization:
        profile["organization"] = organization

    if not profile:
        raise ValueError("At least one profile field must be provided.")

    user = await resolve_user(_client(), login)
    return await _client().update_user(user["id"], profile)


@mcp.tool()
async def deactivate_user(login: str) -> dict[str, str]:
    """
    Deactivate an Okta user account (lifecycle transition to DEPROVISIONED).

    *login* accepts first.last, full email, or Okta user ID.
    """
    user = await resolve_user(_client(), login)
    await _client().deactivate_user(user["id"])
    return {"status": "deactivated", "userId": user["id"], "login": user["profile"]["login"]}


@mcp.tool()
async def activate_user(login: str, send_email: bool = True) -> dict:
    """
    Activate a STAGED or DEPROVISIONED Okta user.

    *login* accepts first.last, full email, or Okta user ID.
    Set *send_email=False* to suppress the activation email and return a token instead.
    """
    user = await resolve_user(_client(), login)
    result = await _client().activate_user(user["id"], send_email)
    return result or {"status": "activated", "userId": user["id"]}


@mcp.tool()
async def suspend_user(login: str) -> dict[str, str]:
    """
    Suspend an ACTIVE Okta user (blocks sign-in without deprovisioning).

    *login* accepts first.last, full email, or Okta user ID.
    """
    user = await resolve_user(_client(), login)
    await _client().suspend_user(user["id"])
    return {"status": "suspended", "userId": user["id"], "login": user["profile"]["login"]}


@mcp.tool()
async def unsuspend_user(login: str) -> dict[str, str]:
    """
    Restore a SUSPENDED user back to ACTIVE.

    *login* accepts first.last, full email, or Okta user ID.
    """
    user = await resolve_user(_client(), login)
    await _client().unsuspend_user(user["id"])
    return {"status": "active", "userId": user["id"], "login": user["profile"]["login"]}


@mcp.tool()
async def unlock_user(login: str) -> dict[str, str]:
    """
    Unlock an Okta user who has been locked out due to failed sign-in attempts.

    *login* accepts first.last, full email, or Okta user ID.
    """
    user = await resolve_user(_client(), login)
    await _client().unlock_user(user["id"])
    return {"status": "unlocked", "userId": user["id"], "login": user["profile"]["login"]}


@mcp.tool()
async def expire_password(login: str) -> dict:
    """
    Expire a user's password so they must reset it on next sign-in.

    *login* accepts first.last, full email, or Okta user ID.
    """
    user = await resolve_user(_client(), login)
    return await _client().expire_password(user["id"])


@mcp.tool()
async def reset_password(login: str, send_email: bool = True) -> dict:
    """
    Trigger a password reset for an Okta user.

    *send_email=True*  – sends the user a reset link via email (default).
    *send_email=False* – returns a one-time reset token instead.

    *login* accepts first.last, full email, or Okta user ID.
    """
    user = await resolve_user(_client(), login)
    result = await _client().reset_password(user["id"], send_email)
    return result or {"status": "reset_initiated", "userId": user["id"]}


@mcp.tool()
async def get_user_groups(login: str) -> list[dict]:
    """
    List all Okta groups that a user belongs to.

    *login* accepts first.last, full email, or Okta user ID.
    """
    user = await resolve_user(_client(), login)
    return await _client().get_user_groups(user["id"])


@mcp.tool()
async def get_user_apps(login: str) -> list[dict]:
    """
    List all Okta app links (application assignments) for a user.

    *login* accepts first.last, full email, or Okta user ID.
    """
    user = await resolve_user(_client(), login)
    return await _client().get_user_app_links(user["id"])


@mcp.tool()
async def get_user_factors(login: str) -> list[dict]:
    """
    List all enrolled MFA factors for an Okta user.

    *login* accepts first.last, full email, or Okta user ID.
    """
    user = await resolve_user(_client(), login)
    return await _client().get_user_factors(user["id"])


@mcp.tool()
async def list_user_sessions(login: str) -> list[dict]:
    """
    List active Okta sessions for a user.

    *login* accepts first.last, full email, or Okta user ID.
    """
    user = await resolve_user(_client(), login)
    return await _client().list_user_sessions(user["id"])


@mcp.tool()
async def clear_user_sessions(login: str) -> dict[str, str]:
    """
    Revoke all active Okta sessions for a user (forces re-authentication).

    *login* accepts first.last, full email, or Okta user ID.
    """
    user = await resolve_user(_client(), login)
    await _client().clear_user_sessions(user["id"])
    return {"status": "sessions_cleared", "userId": user["id"], "login": user["profile"]["login"]}


# =========================================================================
# GROUP MEMBERSHIP
# =========================================================================


@mcp.tool()
async def add_user_to_group(login: str, group_name: str) -> dict[str, str]:
    """
    Add a user to an Okta group.

    *login*      – first.last, full email, or Okta user ID
    *group_name* – display name, short/partial name, or Okta group ID
    """
    c = _client()
    user = await resolve_user(c, login)
    group = await resolve_group(c, group_name)
    await c.add_user_to_group(group["id"], user["id"])
    return {
        "status": "added",
        "userId": user["id"],
        "login": user["profile"]["login"],
        "groupId": group["id"],
        "groupName": group["profile"]["name"],
    }


@mcp.tool()
async def remove_user_from_group(login: str, group_name: str) -> dict[str, str]:
    """
    Remove a user from an Okta group.

    *login*      – first.last, full email, or Okta user ID
    *group_name* – display name, short/partial name, or Okta group ID
    """
    c = _client()
    user = await resolve_user(c, login)
    group = await resolve_group(c, group_name)
    await c.remove_user_from_group(group["id"], user["id"])
    return {
        "status": "removed",
        "userId": user["id"],
        "login": user["profile"]["login"],
        "groupId": group["id"],
        "groupName": group["profile"]["name"],
    }


@mcp.tool()
async def assign_app_to_user(login: str, app_name: str) -> dict:
    """
    Directly assign an Okta application to a user.

    *login*    – first.last, full email, or Okta user ID
    *app_name* – application label, partial name, or Okta app ID
    """
    c = _client()
    user = await resolve_user(c, login)
    app = await resolve_app(c, app_name)
    return await c.assign_app_to_user(app["id"], user["id"])


@mcp.tool()
async def remove_app_from_user(login: str, app_name: str) -> dict[str, str]:
    """
    Remove a direct application assignment from a user.

    *login*    – first.last, full email, or Okta user ID
    *app_name* – application label, partial name, or Okta app ID
    """
    c = _client()
    user = await resolve_user(c, login)
    app = await resolve_app(c, app_name)
    await c.remove_app_from_user(app["id"], user["id"])
    return {
        "status": "removed",
        "userId": user["id"],
        "appId": app["id"],
        "appLabel": app.get("label", ""),
    }


# =========================================================================
# GROUP MANAGEMENT
# =========================================================================


@mcp.tool()
async def list_groups(query: str = "", search: str = "") -> list[dict]:
    """
    List / search Okta groups.

    *query*  – simple name search
    *search* – Okta SCIM filter expression
    """
    return await _client().list_groups(
        q=query or None,
        search=search or None,
    )


@mcp.tool()
async def get_group(group_name: str) -> dict:
    """
    Get an Okta group by display name, partial name, or group ID.
    """
    return await resolve_group(_client(), group_name)


@mcp.tool()
async def create_group(name: str, description: str = "") -> dict:
    """
    Create a new Okta group.
    """
    return await _client().create_group(name, description)


@mcp.tool()
async def update_group(
    group_name: str,
    new_name: str = "",
    description: str = "",
) -> dict:
    """
    Update an Okta group's name or description.

    *group_name* – existing display name, partial name, or group ID
    """
    group = await resolve_group(_client(), group_name)
    return await _client().update_group(
        group["id"],
        name=new_name or None,
        description=description if description != "" else None,
    )


@mcp.tool()
async def delete_group(group_name: str) -> dict[str, str]:
    """
    Delete an Okta group.

    *group_name* – display name, partial name, or group ID
    """
    group = await resolve_group(_client(), group_name)
    await _client().delete_group(group["id"])
    return {"status": "deleted", "groupId": group["id"], "groupName": group["profile"]["name"]}


@mcp.tool()
async def list_group_members(group_name: str) -> list[dict]:
    """
    List all users who are members of an Okta group.

    *group_name* – display name, partial name, or group ID
    """
    group = await resolve_group(_client(), group_name)
    return await _client().list_group_members(group["id"])


@mcp.tool()
async def list_group_apps(group_name: str) -> list[dict]:
    """
    List all applications assigned to an Okta group.

    *group_name* – display name, partial name, or group ID
    """
    group = await resolve_group(_client(), group_name)
    return await _client().list_group_apps(group["id"])


@mcp.tool()
async def assign_app_to_group(app_name: str, group_name: str, priority: int = 0) -> dict:
    """
    Assign an Okta application to a group.

    *app_name*   – application label, partial name, or Okta app ID
    *group_name* – display name, partial name, or Okta group ID
    *priority*   – assignment priority (lower = higher priority)
    """
    c = _client()
    app = await resolve_app(c, app_name)
    group = await resolve_group(c, group_name)
    return await c.assign_group_to_app(app["id"], group["id"], priority)


@mcp.tool()
async def remove_app_from_group(app_name: str, group_name: str) -> dict[str, str]:
    """
    Remove an application assignment from an Okta group.

    *app_name*   – application label, partial name, or Okta app ID
    *group_name* – display name, partial name, or Okta group ID
    """
    c = _client()
    app = await resolve_app(c, app_name)
    group = await resolve_group(c, group_name)
    await c.remove_group_from_app(app["id"], group["id"])
    return {
        "status": "removed",
        "appId": app["id"],
        "groupId": group["id"],
    }


# =========================================================================
# APP MANAGEMENT
# =========================================================================


@mcp.tool()
async def list_apps(query: str = "", filter_expr: str = "") -> list[dict]:
    """
    List / search Okta applications.

    *query*       – simple name/label search
    *filter_expr* – Okta filter expression, e.g. 'status eq "ACTIVE"'
    """
    return await _client().list_apps(
        q=query or None,
        filter_=filter_expr or None,
    )


@mcp.tool()
async def get_app(app_name: str) -> dict:
    """
    Get an Okta application by label, partial name, or app ID.
    """
    return await resolve_app(_client(), app_name)


@mcp.tool()
async def list_app_users(app_name: str) -> list[dict]:
    """
    List all users directly assigned to an Okta application.

    *app_name* – application label, partial name, or Okta app ID
    """
    app = await resolve_app(_client(), app_name)
    return await _client().list_app_users(app["id"])


@mcp.tool()
async def list_app_groups(app_name: str) -> list[dict]:
    """
    List all groups assigned to an Okta application.

    *app_name* – application label, partial name, or Okta app ID
    """
    app = await resolve_app(_client(), app_name)
    return await _client().list_app_groups(app["id"])


# =========================================================================
# SECURITY / AUDIT
# =========================================================================


@mcp.tool()
async def get_security_events(
    since: str = "",
    until: str = "",
    filter_expr: str = "",
    query: str = "",
    limit: int = 100,
) -> list[dict]:
    """
    Query the Okta System Log for security events.

    *since* / *until* – ISO 8601 timestamps, e.g. "2026-06-01T00:00:00Z"
    *filter_expr*     – Okta filter expression, e.g. 'eventType eq "user.session.start"'
    *query*           – free-text search across event fields
    *limit*           – max results (capped at 1000)
    """
    return await _client().get_logs(
        since=since or None,
        until=until or None,
        filter_=filter_expr or None,
        q=query or None,
        limit=limit,
    )


@mcp.tool()
async def get_login_history(login: str, limit: int = 50) -> list[dict]:
    """
    Get recent sign-in events for a specific user from the Okta System Log.

    *login* accepts first.last, full email, or Okta user ID.
    """
    user = await resolve_user(_client(), login)
    actor_id = user["id"]
    return await _client().get_logs(
        filter_=f'actor.id eq "{actor_id}" and eventType eq "user.session.start"',
        limit=limit,
    )


@mcp.tool()
async def get_failed_logins(
    login: str = "",
    since: str = "",
    limit: int = 50,
) -> list[dict]:
    """
    Get failed authentication events, optionally filtered to a single user.

    *login* – optional; first.last, full email, or Okta user ID
    *since* – optional ISO 8601 start timestamp
    *limit* – max results
    """
    c = _client()
    base_filter = 'eventType eq "user.authentication.auth_via_mfa" and outcome.result eq "FAILURE"'

    if login:
        user = await resolve_user(c, login)
        filter_ = f'{base_filter} and actor.id eq "{user["id"]}"'
    else:
        filter_ = base_filter

    return await c.get_logs(
        filter_=filter_,
        since=since or None,
        limit=limit,
    )


# =========================================================================
# ENTRY POINT
# =========================================================================

if __name__ == "__main__":
    mcp.run()
