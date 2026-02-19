import asyncio
import json
import logging

import attr
import websockets

from model import SocketMsg

_q = asyncio.Queue()
_clients = set()


async def handle_connection(websocket):
    _clients.add(websocket)
    logging.info(f"client connected: {websocket.remote_address}")
    try:
        async for msg in websocket:
            pass
    except websockets.exceptions.ConnectionClosed as e:
        logging.info(f"connection closed: {e}")
    finally:
        _clients.remove(websocket)
        logging.info(f"connection closed: {websocket.remote_address}")


async def send_messages():
    while True:
        msg = await _q.get()
        if not msg:
            return
        for client in _clients:
            try:
                await client.send(msg)
                logging.info(f"sent msg to {client.remote_address}")
            except websockets.exceptions.ConnectionClosed:
                _clients.remove(client)


async def send_msg(socket_msg: SocketMsg):
    msg = json.dumps(attr.asdict(socket_msg))
    await _q.put(msg)
