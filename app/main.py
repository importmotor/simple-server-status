from fastapi import FastAPI

from dependencies import token_dependency
from services.sysinfo import get_sys_info
from models.models import SysInfo


app = FastAPI(redoc_url=None, docs_url=None)

@app.get("/", response_model=SysInfo)
async def html_to_pdf(token: token_dependency):
    return get_sys_info()
