from datetime import datetime
from datetime import timezone
from datetime import timedelta
import psutil

from models.models import CpuInfo
from models.models import RamInfo
from models.models import SwapInfo
from models.models import StorageInfo
from models.models import SysInfo
from utils import helpers

 
def get_cpu_info() -> CpuInfo:
    raw_cpu_info = helpers.read_lines('/proc/cpuinfo')
    load_avg = helpers.read_file('/proc/loadavg')
    
    model_name = helpers.search_line(raw_cpu_info, 'model name').split(':')[-1].strip()
    
    cores_str = helpers.search_line(raw_cpu_info, 'cpu cores', "1").split(':')[-1].strip()
    cores = helpers.get_int(cores_str)
    
    threads_str = helpers.search_line(raw_cpu_info, 'siblings', "1").split(':')[-1].strip()
    threads = helpers.get_int(threads_str)
    
    load_avg_split = load_avg.split()
    if len(load_avg_split) != 5:
        load_avg_split = ['0.00', '0.00', '0.00', '0/0']
        
    load_1 = helpers.get_float(load_avg_split[0])
    load_5 = helpers.get_float(load_avg_split[1])
    load_15 = helpers.get_float(load_avg_split[2])
    
    active_processes = helpers.get_int(load_avg_split[3].split('/')[0])
    total_processes = helpers.get_int(load_avg_split[3].split('/')[-1])
    
    cpu_freq_str = helpers.search_line(raw_cpu_info, "cpu MHz", "0").split(':')[-1].strip()
    cpu_freq = int(helpers.get_int(cpu_freq_str) / 1024)
        
    return CpuInfo(
        model=model_name,
        cores=cores,
        threads=threads,
        load_1=load_1,
        load_5=load_5,
        load_15=load_15,
        percent=psutil.cpu_percent(interval=0.2),
        active_processes=active_processes,
        total_processes=total_processes,
        freq=cpu_freq,
    )

def get_mem_info() -> RamInfo:
    raw_mem_info = helpers.read_lines('/proc/meminfo')
    
    total_str = helpers.search_line(raw_mem_info, 'MemTotal').split(":")[-1].strip()
    total = int(int(total_str.split()[0]) / 1024)
    
    available_str = helpers.search_line(raw_mem_info, 'MemAvailable').split(":")[-1].strip()
    available = int(int(available_str.split()[0]) / 1024)
    
    used = total - available
    percent = round((used / (total + 1)) * 100, 1)
    
    return RamInfo(
        total=total,
        available=available,
        used=used,
        percent=percent,
    )

def get_swap_info() -> SwapInfo:
    raw_swap_info = helpers.read_lines('/proc/swaps')[-1]
    raw_swap_info_split = raw_swap_info.split()
    if len(raw_swap_info_split) != 5:
        return SwapInfo(
            total=0,
            used=0,
            free=0,
            percent=0,
        )
    
    swap_total = int(helpers.get_int(raw_swap_info.split()[2]) / 1024)
    swap_used = int(helpers.get_int(raw_swap_info.split()[3]) / 1024)
    swap_free = swap_total - swap_used
    swap_percent = round((swap_used / (swap_total + 1)) * 100, 1)
    
    return SwapInfo(
        total=swap_total,
        used=swap_used,
        free=swap_free,
        percent=swap_percent,
    )
    
def get_storage_info() -> StorageInfo:
    mount_point = "/"
    raw_storage_info_line = helpers.exec_command(f'df -h {mount_point}').splitlines()[-1]
    raw_storage_info_split = raw_storage_info_line.split()
    if len(raw_storage_info_split) != 6:
        return StorageInfo(
            total=0,
            used=0,
            free=0,
            percent=0,
            mountpoint=mount_point,
        )
    
    return StorageInfo(
        total=helpers.get_int(raw_storage_info_split[1]),
        used=helpers.get_int(raw_storage_info_split[2]),
        free=helpers.get_int(raw_storage_info_split[3]),
        percent=helpers.get_int(raw_storage_info_split[4]),
        mountpoint=mount_point,
    )
    
def get_sys_info() -> SysInfo:
    uptime = helpers.read_lines('/proc/uptime')
    uptime_seconds = int(float(uptime[0].split()[0]))
    
    
    return SysInfo(
        created_at=datetime.now(timezone.utc),
        started_at=datetime.fromtimestamp(psutil.boot_time(), timezone.utc),
        uptime=timedelta(seconds=uptime_seconds),
        cpu=get_cpu_info(),
        ram=get_mem_info(),
        storage=get_storage_info(),
        swap=get_swap_info(),
    )
    
