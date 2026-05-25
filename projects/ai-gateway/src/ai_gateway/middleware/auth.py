from __future__ import annotations

from secrets import compare_digest

from fastapi import HTTPException, Request


class AuthMiddleware:
    def __init__(self, api_keys: list[str], enabled: bool = True) -> None:
        self.api_keys = set(api_keys)
        self.enabled = enabled

    async def __call__(self, request: Request) -> str | None:
        if not self.enabled:
            return None

        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise HTTPException(
                status_code=401,
                detail={
                    "message": "Missing Authorization header",
                    "type": "authentication_error",
                    "code": "401",
                },
            )

        if not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=401,
                detail={
                    "message": "Invalid Authorization header format. Expected: Bearer <key>",
                    "type": "authentication_error",
                    "code": "401",
                },
            )

        token = auth_header[7:]
        if not any(compare_digest(token, api_key) for api_key in self.api_keys):
            raise HTTPException(
                status_code=401,
                detail={
                    "message": "Invalid API key",
                    "type": "authentication_error",
                    "code": "401",
                },
            )
        return token


async def verify_bearer_token(request: Request) -> str | None:
    config = getattr(request.app.state, "config", None)
    if config is None:
        from ai_gateway.config import get_config

        config = get_config()
    middleware = AuthMiddleware(
        api_keys=config.auth.api_keys,
        enabled=config.auth.enabled,
    )
    return await middleware(request)
