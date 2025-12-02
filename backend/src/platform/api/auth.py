from __future__ import annotations

import asyncio
import logging
import os
import time
from typing import Optional

import httpx

from src.platform.db.schema import TemplateEnvironment

logger = logging.getLogger(__name__)


ENVIRONMENT = os.getenv("ENVIRONMENT", "development").lower()
CONTROL_PLANE_URL = os.getenv("CONTROL_PLANE_URL")
CONTROL_PLANE_TIMEOUT = float(os.getenv("CONTROL_PLANE_TIMEOUT", "10.0"))
API_KEY_CACHE_TTL = int(os.getenv("API_KEY_CACHE_TTL", "300"))

_http_client: httpx.AsyncClient | None = None
_http_client_lock = asyncio.Lock()

_api_key_cache: dict[str, tuple[str, float]] = {}  # api_key -> (user_id, expires_at)


def is_dev_mode() -> bool:
    """Check if running in development mode."""
    return ENVIRONMENT == "development"


async def _get_http_client() -> httpx.AsyncClient:
    """Get or create shared HTTP client with connection pooling."""
    global _http_client
    if _http_client is None or _http_client.is_closed:
        async with _http_client_lock:
            if _http_client is None or _http_client.is_closed:
                _http_client = httpx.AsyncClient(
                    timeout=CONTROL_PLANE_TIMEOUT,
                    limits=httpx.Limits(
                        max_connections=100, max_keepalive_connections=20
                    ),
                )
    return _http_client


def _get_cached_user_id(api_key: str) -> str | None:
    """Get cached user_id for API key if still valid."""
    if api_key in _api_key_cache:
        user_id, expires_at = _api_key_cache[api_key]
        if time.time() < expires_at:
            return user_id
        else:
            del _api_key_cache[api_key]
    return None


def _cache_user_id(api_key: str, user_id: str) -> None:
    """Cache user_id for API key."""
    _api_key_cache[api_key] = (user_id, time.time() + API_KEY_CACHE_TTL)


async def validate_with_control_plane(api_key: str, action: str = "api_request") -> str:
    """
    Validate API key with control plane and return principal_id.


    Args:
        api_key: The API key to validate
        action: The action being performed ('api_request' or 'environment_created')
    """
    if not CONTROL_PLANE_URL:
        raise RuntimeError("CONTROL_PLANE_URL not configured for production mode")

    # Check cache first (skip for environment_created to always track usage)
    if action == "api_request":
        cached_user_id = _get_cached_user_id(api_key)
        if cached_user_id:
            return cached_user_id

    try:
        client = await _get_http_client()
        response = await client.post(
            f"{CONTROL_PLANE_URL}/validate",
            json={"api_key": api_key, "action": action},
        )

        if response.status_code == 200:
            data = response.json()
            if data.get("valid"):
                user_id = data["user_id"]
                _cache_user_id(api_key, user_id)
                return user_id
            else:
                raise PermissionError(data.get("reason", "access denied"))
        elif response.status_code == 401:
            raise PermissionError("invalid api key")
        elif response.status_code == 429:
            raise PermissionError("rate limit exceeded")
        else:
            raise PermissionError(f"authorization failed: {response.status_code}")

    except httpx.TimeoutException:
        raise PermissionError("control plane timeout - try again")
    except httpx.RequestError as e:
        raise RuntimeError(f"control plane unavailable: {e}")


async def get_principal_id(api_key: Optional[str], action: str = "api_request") -> str:
    """
    Get the principal (user) ID from API key.

    Args:
        api_key: The API key to validate
        action: The action being performed ('api_request' or 'environment_created')
    """
    if is_dev_mode():
        return "dev-user"

    if not api_key:
        raise PermissionError("api key required in production mode")

    # Strip "Bearer " prefix if present
    clean_key = api_key
    if api_key.lower().startswith("bearer "):
        clean_key = api_key[7:]  # Remove "Bearer " (7 chars)

    return await validate_with_control_plane(clean_key, action)


def require_resource_access(principal_id: str, owner_id: str) -> None:
    """Require principal can access resource, raise PermissionError if not."""

    if is_dev_mode() or principal_id == owner_id:
        return

    raise PermissionError("unauthorized")


def check_template_access(principal_id: str, template: TemplateEnvironment) -> None:
    """Check if principal can access template."""
    if template.visibility == "public":
        return
    if template.owner_id and template.owner_id == principal_id:
        return
    raise PermissionError("unauthorized")
