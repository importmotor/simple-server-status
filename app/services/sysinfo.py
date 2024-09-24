from datetime import datetime
from datetime import timezone
from subprocess import run

from models.models import CpuInfo
from models.models import MemInfo
from models.models import SwapInfo
from models.models import SysInfo


def _read_file(file_path: str) -> str:
    with open(file_path, 'r') as file:
        lines = file.readlines()
        return [line.strip() for line in lines]
    
def _search_value(lines: list[str], key: str, default: str = "") -> str:
    for line in lines:
        if key in line:
            return line.split(':')[1].strip()
    return default

def _exec_command(command: str) -> str:
    return run(command.split(" "), capture_output=True, text=True).stdout

def _get_processes() -> list[str]:
    processes = _exec_command('ps -eo pid,ppid,cmd,%mem,%cpu --sort=-%cpu').split('\n')
    return [process.strip() for process in processes][1:]
    
def get_cpu_info() -> CpuInfo:
    raw_cpu_info = _read_file('/proc/cpuinfo')
    
    return CpuInfo(
        model=_search_value(raw_cpu_info, 'model name'),
        cores=int(_search_value(raw_cpu_info, 'cpu cores', "1")),
        threads=int(_search_value(raw_cpu_info, 'siblings', "1")),
        load=" ".join(_read_file('/proc/loadavg')),
        freq=int(float(_search_value(raw_cpu_info, 'cpu MHz'))),
    )

def get_mem_info() -> MemInfo:
    raw_mem_info = _read_file('/proc/meminfo')
    
    total = int(int(_search_value(raw_mem_info, 'MemTotal').split()[0]) / 1024)
    available = int(int(_search_value(raw_mem_info, 'MemAvailable').split()[0]) / 1024)
    used = total - available
    free = available
    percent = round((used / total) * 100, 1)
    
    return MemInfo(
        total=total,
        available=available,
        used=used,
        free=free,
        percent=percent,
    )

def get_swap_info() -> SwapInfo:
    raw_swap_info = _read_file('/proc/swaps')[1]
    
    swap_total = int(int(raw_swap_info.split()[2]) / 1024)
    swap_used = int(int(raw_swap_info.split()[3]) / 1024)
    swap_free = swap_total - swap_used
    swap_percent = round((swap_used / swap_total) * 100, 1)
    
    return SwapInfo(
        total=swap_total,
        used=swap_used,
        free=swap_free,
        percent=swap_percent,
    )
    
def get_sys_info() -> SysInfo:
    
    return SysInfo(
        created_at=datetime.now(timezone.utc),
        uptime=" ".join(_read_file('/proc/uptime')),
        uptime_pretty=_exec_command('uptime -p').strip(),
        cpu=get_cpu_info(),
        memory=get_mem_info(),
        swap=get_swap_info(),
        processes=_get_processes(),
    )
    
