from fastapi.datastructures import URL
from fastapi.responses import RedirectResponse
from starlette.types import ASGIApp, Receive, Scope, Send


class RedirectsMiddleware:
    """
    Redirect a specified path to another path

    Example Usage:
    .. code-block:: python

        redirections = {
            "/v1/resource/": "/v2/resource/",
            # ...
        }

        middleware = [
            Middleware(RedirectsMiddleware, path_mapping=redirections),
        ]

        app = Starlette(routes=routes, middleware=middleware)
    """

    def __init__(self, app: ASGIApp, path_mapping: dict) -> None:
        self.app = app
        self.path_mapping = path_mapping

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        url = URL(scope=scope)

        if url.path in self.path_mapping:
            url = url.replace(path=self.path_mapping[url.path])
            response = RedirectResponse(url, status_code=301)
            await response(scope, receive, send)
            return

        await self.app(scope, receive, send)
