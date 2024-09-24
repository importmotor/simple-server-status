from __future__ import annotations

from dataclasses import dataclass
from os import getenv


@dataclass(frozen=True)
class Config:
    ACCESS_TOKEN: str
    
    @staticmethod
    def load_config() -> Config:
        access_token = getenv("ACCESS_TOKEN", "")
            
        return Config(access_token)
    
CONFIG = Config.load_config()