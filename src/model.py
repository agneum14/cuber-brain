from enum import StrEnum, auto

from attr import define


class Tool(StrEnum):
    video = auto()
    shader = auto()


@define
class VideoPayload:
    name: str


@define
class ShaderPayload:
    name: str


@define
class SocketMsg:
    tool: Tool
    payload: VideoPayload | ShaderPayload
