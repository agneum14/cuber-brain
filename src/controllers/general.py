from fastapi import APIRouter

from model import ShaderPayload, SocketMsg, Tool, VideoPayload
from ws_server import send_msg

router = APIRouter(prefix="/general", tags=["general"])


@router.post("/setVideo", description="Set video with socket message.")
async def setVideo(name: str):
    payload = VideoPayload(name)
    socket_msg = SocketMsg(Tool.video, payload)
    await send_msg(socket_msg)


@router.post("/setShader", description="Set shader with socket message.")
async def setShader(name: str):
    payload = ShaderPayload(name)
    socket_msg = SocketMsg(Tool.shader, payload)
    await send_msg(socket_msg)
