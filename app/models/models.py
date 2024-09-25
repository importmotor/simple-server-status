from dataclasses import dataclass
from datetime import datetime
from datetime import timedelta


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
    total: int
    used: int
    free: int
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
