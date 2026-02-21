from enum import StrEnum, auto

import requests
from attrs import define
from bs4 import BeautifulSoup

from config import get_config


def _names(url: str) -> [str]:
    res = requests.get(url)
    soup = BeautifulSoup(res.content, "html.parser")
    return [x.text.rsplit(".", 1)[0] for x in soup.select("pre a")[1:]]


def video_names() -> [str]:
    url = get_config().fs_base_url() + "/videos/"
    return _names(url)


def shader_names() -> [str]:
    url = get_config().fs_base_url() + "/shaders/"
    return [""] + _names(url)


class Tool(StrEnum):
    video = auto()
    shader = auto()
    video_speed = auto()


@define
class VideoPayload:
    name: str


@define
class ShaderPayload:
    name: str


@define
class VideoSpeedPayload:
    speed: float


@define
class SocketMsg:
    tool: Tool
    payload: VideoPayload | ShaderPayload | VideoSpeedPayload
