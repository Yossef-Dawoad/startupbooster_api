import time

from starlette.types import ASGIApp, Message, Receive, Scope, Send


class TimedRequestASGIMiddleware:
    """
    Inject `x-process-time` header into the responses
    """

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "http":
            start_time = time.time()
            send_headers = await self.send_wrapper(send, start_time)
            await self.app(scope, receive, send_headers)
        else:
            await self.app(scope, receive, send)

    async def send_wrapper(self, send: Send, start_time: float) -> None:
        async def wrapper(message: Message) -> None:
            if message["type"] == "http.response.start":
                process_time = time.time() - start_time
                message["headers"].append(
                    (b"x-process-time", str(process_time).encode()),
                )
            await send(message)

        return wrapper
