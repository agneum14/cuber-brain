import asyncio
from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

from model import (
    NavigateKind,
    NavigatePayload,
    ShaderPayload,
    SocketMsg,
    Tool,
    VideoPayload,
    VideoSpeedPayload,
    shader_names,
    video_names,
)
from ws_server import send_msg

router = APIRouter(prefix="/general", tags=["general"])


async def send_msg_batch(msgs: List[SocketMsg]):
    await asyncio.gather(*[send_msg(x) for x in msgs])


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


class NavigateModel(BaseModel):
    kind: NavigateKind
    name: str


@router.post("/navigate", description="Navigate to a kind of page.")
async def navigate(input: NavigateModel):
    msg = SocketMsg(Tool.navigate, NavigatePayload(input.kind, input.name))
    await send_msg(msg)


class ConfigureVideoModel(BaseModel):
    videoName: str
    shaderName: str
    speed: float


@router.post("/configureVideo", description="Configure the entire video state.")
async def configureVideo(input: ConfigureVideoModel):
    msgs = [
        SocketMsg(Tool.navigate, NavigatePayload(NavigateKind.VIDEO, "")),
        SocketMsg(Tool.video, VideoPayload(input.videoName)),
        SocketMsg(Tool.shader, ShaderPayload(input.shaderName)),
        SocketMsg(Tool.video_speed, VideoSpeedPayload(input.speed)),
    ]
    await send_msg_batch(msgs)


@router.get("/availableVideos", description="Get the available videos.")
def availableVideos() -> List[str]:
    return video_names()


@router.get("/availableShaders", description="Get the available shaders.")
def availableShaders() -> List[str]:
    return shader_names()
