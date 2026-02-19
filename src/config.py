import os

from attrs import define

_config = None


@define(frozen=True)
class Config:
    port: int
    addr: str
    api_port: int
    api_addr: str
    fs_port: int
    fs_addr: str

    @classmethod
    def create(cls):
        port = int(os.getenv("CUBER_BRAIN_PORT", "7070"))
        addr = os.getenv("CUBER_BRAIN_HOST", "0.0.0.0")
        api_port = int(os.getenv("CUBER_BRAIN_API_PORT", "8081"))
        api_addr = os.getenv("CUBER_BRAIN_API_HOST", "0.0.0.0")
        fs_port = int(os.getenv("CUBER_BRAIN_FS_PORT", "8080"))
        fs_addr = os.getenv("CUBER_BRAIN_FS_HOST", "localhost")
        return cls(port, addr, api_port, api_addr, fs_port, fs_addr)

    def fs_base_url(self) -> str:
        return f"http://{self.fs_addr}:{self.fs_port}"


def get_config() -> Config:
    global _config
    if not _config:
        _config = Config.create()
    return _config
