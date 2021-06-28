import json
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from bson import json_util

from src.models.models import RouterRequest

router = APIRouter(
    #dependencies=[Depends(get_token_header)],
    prefix='/router',
    responses={404: {"description": "Not found"}},
)

@router.post('/hello')
async def get_router_response(request: RouterRequest):
    if not request.name:
        return {"router": "says hello"}
    return {"router": f"welcome back {request.name}"}
