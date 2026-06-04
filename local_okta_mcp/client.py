"""Thin async wrapper around the Okta management REST API."""

import os
from typing import Any
import httpx


class OktaError(Exception):
    def __init__(self, status: int, message: str):
        self.status = status
        super().__init__(f"Okta API {status}: {message}")


class OktaClient:
    def __init__(self):
        org_url = os.environ["OKTA_CLIENT_ORGURL"].rstrip("/")
        token = os.environ["OKTA_API_TOKEN"]
        self._base = f"{org_url}/api/v1"
        self._headers = {
            "Authorization": f"SSWS {token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    # ------------------------------------------------------------------
    # internal helpers
    # ------------------------------------------------------------------

    async def _request(
        self,
        method: str,
        path: str,
        params: dict | None = None,
        json: Any = None,
    ) -> Any:
        url = f"{self._base}{path}"
        async with httpx.AsyncClient(timeout=30) as http:
            resp = await http.request(
                method, url, headers=self._headers, params=params, json=json
            )
        if resp.status_code >= 400:
            try:
                detail = resp.json().get("errorSummary", resp.text)
            except Exception:
                detail = resp.text
            raise OktaError(resp.status_code, detail)
        if resp.status_code == 204 or not resp.content:
            return None
        return resp.json()

    async def _paginate(self, path: str, params: dict | None = None) -> list:
        """Follow Okta link-header pagination and collect all items."""
        params = dict(params or {})
        params.setdefault("limit", 200)
        url = f"{self._base}{path}"
        results = []
        async with httpx.AsyncClient(timeout=30) as http:
            while url:
                resp = await http.get(url, headers=self._headers, params=params)
                if resp.status_code >= 400:
                    try:
                        detail = resp.json().get("errorSummary", resp.text)
                    except Exception:
                        detail = resp.text
                    raise OktaError(resp.status_code, detail)
                results.extend(resp.json())
                link = resp.headers.get("link", "")
                url = _next_link(link)
                params = {}  # params already encoded in next URL
        return results

    # ------------------------------------------------------------------
    # users
    # ------------------------------------------------------------------

    async def list_users(self, q: str | None = None, search: str | None = None, filter_: str | None = None) -> list:
        params: dict[str, Any] = {}
        if q:
            params["q"] = q
        if search:
            params["search"] = search
        if filter_:
            params["filter"] = filter_
        return await self._paginate("/users", params)

    async def get_user(self, user_id: str) -> dict:
        return await self._request("GET", f"/users/{user_id}")

    async def create_user(self, profile: dict, credentials: dict | None = None, activate: bool = True) -> dict:
        body: dict[str, Any] = {"profile": profile}
        if credentials:
            body["credentials"] = credentials
        return await self._request("POST", "/users", params={"activate": str(activate).lower()}, json=body)

    async def update_user(self, user_id: str, profile: dict) -> dict:
        return await self._request("POST", f"/users/{user_id}", json={"profile": profile})

    async def deactivate_user(self, user_id: str) -> None:
        await self._request("POST", f"/users/{user_id}/lifecycle/deactivate")

    async def activate_user(self, user_id: str, send_email: bool = True) -> dict | None:
        return await self._request("POST", f"/users/{user_id}/lifecycle/activate", params={"sendEmail": str(send_email).lower()})

    async def suspend_user(self, user_id: str) -> None:
        await self._request("POST", f"/users/{user_id}/lifecycle/suspend")

    async def unsuspend_user(self, user_id: str) -> None:
        await self._request("POST", f"/users/{user_id}/lifecycle/unsuspend")

    async def unlock_user(self, user_id: str) -> None:
        await self._request("POST", f"/users/{user_id}/lifecycle/unlock")

    async def expire_password(self, user_id: str) -> dict:
        return await self._request("POST", f"/users/{user_id}/lifecycle/expire_password")

    async def reset_password(self, user_id: str, send_email: bool = True) -> dict | None:
        return await self._request("POST", f"/users/{user_id}/lifecycle/reset_password", params={"sendEmail": str(send_email).lower()})

    async def get_user_groups(self, user_id: str) -> list:
        return await self._paginate(f"/users/{user_id}/groups")

    async def get_user_app_links(self, user_id: str) -> list:
        return await self._paginate(f"/users/{user_id}/appLinks")

    async def get_user_factors(self, user_id: str) -> list:
        return await self._paginate(f"/users/{user_id}/factors")

    async def list_user_sessions(self, user_id: str) -> list:
        return await self._request("GET", f"/users/{user_id}/sessions")

    async def clear_user_sessions(self, user_id: str) -> None:
        await self._request("DELETE", f"/users/{user_id}/sessions")

    # ------------------------------------------------------------------
    # group membership
    # ------------------------------------------------------------------

    async def add_user_to_group(self, group_id: str, user_id: str) -> None:
        await self._request("PUT", f"/groups/{group_id}/users/{user_id}")

    async def remove_user_from_group(self, group_id: str, user_id: str) -> None:
        await self._request("DELETE", f"/groups/{group_id}/users/{user_id}")

    async def assign_app_to_user(self, app_id: str, user_id: str, profile: dict | None = None) -> dict:
        body: dict[str, Any] = {"id": user_id, "scope": "USER"}
        if profile:
            body["profile"] = profile
        return await self._request("POST", f"/apps/{app_id}/users", json=body)

    async def remove_app_from_user(self, app_id: str, user_id: str) -> None:
        await self._request("DELETE", f"/apps/{app_id}/users/{user_id}")

    # ------------------------------------------------------------------
    # groups
    # ------------------------------------------------------------------

    async def list_groups(self, q: str | None = None, search: str | None = None) -> list:
        params: dict[str, Any] = {}
        if q:
            params["q"] = q
        if search:
            params["search"] = search
        return await self._paginate("/groups", params)

    async def get_group(self, group_id: str) -> dict:
        return await self._request("GET", f"/groups/{group_id}")

    async def create_group(self, name: str, description: str = "") -> dict:
        return await self._request("POST", "/groups", json={"profile": {"name": name, "description": description}})

    async def update_group(self, group_id: str, name: str | None = None, description: str | None = None) -> dict:
        profile: dict[str, str] = {}
        if name:
            profile["name"] = name
        if description is not None:
            profile["description"] = description
        return await self._request("PUT", f"/groups/{group_id}", json={"profile": profile})

    async def delete_group(self, group_id: str) -> None:
        await self._request("DELETE", f"/groups/{group_id}")

    async def list_group_members(self, group_id: str) -> list:
        return await self._paginate(f"/groups/{group_id}/users")

    async def list_group_apps(self, group_id: str) -> list:
        return await self._paginate(f"/groups/{group_id}/apps")

    # ------------------------------------------------------------------
    # apps
    # ------------------------------------------------------------------

    async def list_apps(self, q: str | None = None, filter_: str | None = None) -> list:
        params: dict[str, Any] = {}
        if q:
            params["q"] = q
        if filter_:
            params["filter"] = filter_
        return await self._paginate("/apps", params)

    async def get_app(self, app_id: str) -> dict:
        return await self._request("GET", f"/apps/{app_id}")

    async def list_app_users(self, app_id: str) -> list:
        return await self._paginate(f"/apps/{app_id}/users")

    async def list_app_groups(self, app_id: str) -> list:
        return await self._paginate(f"/apps/{app_id}/groups")

    async def assign_group_to_app(self, app_id: str, group_id: str, priority: int = 0) -> dict:
        return await self._request("PUT", f"/apps/{app_id}/groups/{group_id}", json={"priority": priority})

    async def remove_group_from_app(self, app_id: str, group_id: str) -> None:
        await self._request("DELETE", f"/apps/{app_id}/groups/{group_id}")

    # ------------------------------------------------------------------
    # security / system log
    # ------------------------------------------------------------------

    async def get_logs(
        self,
        since: str | None = None,
        until: str | None = None,
        filter_: str | None = None,
        q: str | None = None,
        limit: int = 100,
    ) -> list:
        params: dict[str, Any] = {"limit": min(limit, 1000)}
        if since:
            params["since"] = since
        if until:
            params["until"] = until
        if filter_:
            params["filter"] = filter_
        if q:
            params["q"] = q
        return await self._paginate("/logs", params)


def _next_link(link_header: str) -> str | None:
    """Extract the `next` URL from an Okta link header."""
    for part in link_header.split(","):
        part = part.strip()
        if 'rel="next"' in part:
            url_part = part.split(";")[0].strip()
            if url_part.startswith("<") and url_part.endswith(">"):
                return url_part[1:-1]
    return None
