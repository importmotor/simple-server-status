from threading import Thread
from threading import Event
from threading import Lock
from time import sleep

from services.sysinfo import get_sys_info
from models.models import SysInfo
from models.models import Config


class BackgroundInfo:
    def __init__(self):
        self._config = Config.load()
        self._stop_event = Event()
        self._sysinfo = SysInfo.get_init()
        self._lock = Lock()
        
        self._start()
    
    def _update_loop(self):
        while not self._stop_event.is_set():
            try:
                self._sysinfo = get_sys_info(self._config.collection_time)
            except Exception as e:
                print("Error updating sysinfo:")
                print(e)
                print("Continuing...")
                
            sleep(self._config.sleep_time)
            
    def _start(self):
        self._thread = Thread(target=self._update_loop, daemon=True)
        self._thread.start()
        
    def stop(self):
        self._stop_event.set()
        self._thread.join()
    
    def set_sleep_time(self, sleep_time: float):
        self._config.sleep_time = sleep_time
        self._config.save()
    
    def set_collection_time(self, collection_time: float):
        self._config.collection_time = collection_time
        self._config.save()
        
    @property
    def config(self):
        return self._config
    
    @property
    def sysinfo(self):
        with self._lock:
            return self._sysinfo