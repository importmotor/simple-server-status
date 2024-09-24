from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from datetime import timezone


@dataclass(frozen=True)
class CpuInfo:
    model: str
    cores: int
    threads: int
    load: str
    freq: float
    
@dataclass(frozen=True)
class MemInfo:
    total: int
    available: int
    used: int
    free: int
    percent: float
    
@dataclass(frozen=True)
class SwapInfo:
    total: int
    used: int
    free: int
    percent: float
    
@dataclass(frozen=True)
class SysInfo:
    created_at: datetime
    uptime: str
    uptime_pretty: str
    cpu: CpuInfo
    memory: MemInfo
    swap: SwapInfo
    processes: list[str]
