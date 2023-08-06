import logging
import socket

import discord
from aiohttp import web

logger = logging.getLogger(__name__)


class Healthcheck:
    def __init__(
        self, client: discord.Client, host: str = "0.0.0.0", port: int = 8080
    ) -> None:
        self.host = host
        self.port = port
        self.client = client

    async def handle(self, request) -> web.Response:
        text: str = f"Client is ready: {self.client.is_ready()}"
        return web.Response(text=text)

    def create_socket(self, reuse_port: bool = False) -> socket.socket:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if reuse_port:
            sock.setsockopt(socket.SOL_SOCKET, 15, 1)
        sock.bind((self.host, self.port))
        return sock

    async def start_server(self) -> None:
        app = web.Application()
        app.add_routes([web.get("/", self.handle)])

        runner = web.AppRunner(app)
        await runner.setup()

        sock = self.create_socket(reuse_port=True)

        server = web.SockSite(runner, sock)
        await server.start()

        logger.info("Listening on port %d", self.port)
