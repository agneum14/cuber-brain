import asyncio
import logging

import uvicorn
import websockets

from api import app
from config import get_config
from ws_server import handle_connection, send_messages


def conf_logging():
    logging.basicConfig(level=logging.INFO)


async def main():
    conf_logging()

    server = await websockets.serve(
        handle_connection, get_config().addr, get_config().port
    )
    asyncio.create_task(send_messages())

    uconfig = uvicorn.Config(
        app, host=get_config().api_addr, port=get_config().api_port, reload=True
    )
    userver = uvicorn.Server(uconfig)

    tasks = [asyncio.create_task(x) for x in [userver.serve(), server.wait_closed()]]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
