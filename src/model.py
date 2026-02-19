import json
from enum import StrEnum, auto
from typing import Literal

import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel

from config import get_config


def _names(url: str) -> [str]:
    res = requests.get(url)
    soup = BeautifulSoup(res.content, "html.parser")
    return [x.text.rsplit(".", 1)[0] for x in soup.select("pre a")[1:]]


def _video_names() -> [str]:
    url = get_config().fs_base_url() + "/videos/"
    return _names(url)


def _shader_names() -> [str]:
    url = get_config().fs_base_url() + "/shaders/"
    return _names(url)


class Tool(StrEnum):
    video = auto()
    shader = auto()


class VideoPayload(BaseModel):
    name: Literal[tuple(_video_names())]


class ShaderPayload(BaseModel):
    name: Literal[tuple(_shader_names())]


class SocketMsg(BaseModel):
    tool: Tool
    payload: VideoPayload | ShaderPayload


def socket_msg_schema() -> str:
    return json.dumps(SocketMsg.model_json_schema(), indent=2)


if __name__ == "__main__":
    print(socket_msg_schema())
