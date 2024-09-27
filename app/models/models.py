from __future__ import annotations
from dataclasses import dataclass
from dataclasses import asdict
from json import dumps
from json import loads
from datetime import datetime
from datetime import timedelta
from os.path import exists


@dataclass(frozen=True)
class CpuInfo:
    model: str
    cores: int
    threads: int
    load_1: float
    load_5: float
    load_15: float
    percent: float
    active_processes: int
    total_processes: int
    freq: float
    
@dataclass(frozen=True)
class RamInfo:
    total: int
    used: int
    available: int
    percent: float
    
@dataclass(frozen=True)
class SwapInfo:
    total: int
    used: int
    free: int
    percent: float
    
@dataclass(frozen=True)
class StorageInfo:
    total: float
    used: float
    free: float
    percent: float
    mountpoint: str

@dataclass(frozen=True)
class SysInfo:
    server_name: str
    created_at: datetime
    started_at: datetime
    uptime: timedelta
    cpu: CpuInfo
    ram: RamInfo
    storage: StorageInfo
    swap: SwapInfo
    
    @staticmethod
    def get_init() -> SysInfo:
        return SysInfo(
            "", 
            datetime.now(), 
            datetime.now(), 
            timedelta(seconds=0), 
            CpuInfo("", 0, 0, 0, 0, 0, 0, 0, 0, 0), 
            RamInfo(0, 0, 0, 0), 
            StorageInfo(0, 0, 0, 0, ""), 
            SwapInfo(0, 0, 0, 0)
        )

@dataclass()
class Config:
    _default_config_path = "./config.json"
    collection_time: float
    sleep_time: float
    
    def save(self):
        dict_config = asdict(self)
        with open(Config._default_config_path, "w") as file:
            file.write(dumps(dict_config))

    @staticmethod
    def load() -> Config:
        if not exists(Config._default_config_path):
            config = Config(20, 30)
            config.save()
            return config
        
        with open(Config._default_config_path, "r") as file:
            dict_config = loads(file.read())
            return Config(**dict_config)
