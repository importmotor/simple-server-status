from __future__ import annotations

from dataclasses import dataclass
from os import getenv


@dataclass(frozen=True)
class Config:
    SERVER_NAME: str
    ACCESS_TOKEN: str
    
    @staticmethod
    def load_config() -> Config:
        server_name = getenv("SERVER_NAME", "")
        access_token = getenv("ACCESS_TOKEN", "")
            
        return Config(server_name, access_token)
    
CONFIG = Config.load_config()