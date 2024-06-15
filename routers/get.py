from fastapi import APIRouter

from util.logWriter import logWriter



router = APIRouter()

@router.get("/getJwt")
def getJwt():
    print(1234)