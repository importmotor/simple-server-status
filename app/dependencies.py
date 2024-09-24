from typing import Annotated

from fastapi import Depends
from fastapi import Request
from fastapi import HTTPException

from utils.config import CONFIG


async def check_token(req: Request) -> str:
    global CONFIG
    
    user_token = req.query_params.get('key')
    if user_token != CONFIG.ACCESS_TOKEN:
        raise HTTPException(status_code=403, detail="key is invalid")
    
    return user_token

token_dependency = Annotated[str, Depends(check_token)]