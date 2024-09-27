from fastapi import FastAPI
from fastapi import Query
from fastapi.openapi.docs import get_swagger_ui_html

from dependencies import token_dependency
from models.models import SysInfo
from models.models import Config
from services.background_info import BackgroundInfo


app = FastAPI(redoc_url=None, docs_url=None)
info = BackgroundInfo()


@app.get("/docs", include_in_schema=False)
async def show_docs(token: token_dependency):
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")

@app.get("/", response_model=SysInfo)
async def status(token: token_dependency):
    return info.sysinfo

@app.get("/config", response_model=Config)
async def get_config(token: token_dependency):
    return info.config

@app.patch("/config", response_model=Config)
async def set_config(token: token_dependency, collection_time:float = Query(le=120, ge=1), sleep_time:float = Query(le=300, ge=0.1)):
    info.set_collection_time(collection_time)
    info.set_sleep_time(sleep_time)
    
    return info.config