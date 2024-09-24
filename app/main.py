from datetime import datetime
from datetime import timezone

from fastapi import FastAPI
from dependencies import token_dependency
from services.sysinfo import get_sys_info


app = FastAPI(redoc_url=None)

@app.get("/")
# async def html_to_pdf(token: token_dependency):
async def html_to_pdf():
    return get_sys_info()
