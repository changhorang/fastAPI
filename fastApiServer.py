import uvicorn
import logging
import os
import argparse

from util.logWriter import logWriter
import routers.get as get


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


# def load_config():
#     # 설정 파일에서 값을 읽어와서 전역 변수에 저장
#     with open("config.yaml", "r") as f:
#         global config
#         config = yaml.safe_load(f)
   
#     return config


def access_log() :
    ''' 엑세스 로그 포맷은 다음과 같이 지정'''
    logger = logging.getLogger('uvicorn.access')
    console_formatter = uvicorn.logging.ColourizedFormatter(
        "{asctime} - {message}",
        style="{", use_colors=True)
    handler = logging.handlers.TimedRotatingFileHandler(f"./fastApiServer.log", when='midnight', interval=1, backupCount=1)
    handler.setFormatter(console_formatter)
    logger.addHandler(handler)


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Access-Control-Allow-Private-Network"],
)


app.include_router(get.router, tags=["GET"])


@app.on_event("startup")
async def startup_event():
    logWriter.log.info(f"START UP ENGINE : {ENG_NAME}")
    access_log()


@app.on_event("shutdown")
async def shutdown_event():
    logWriter.log.info(f"SHUT DOWN ENGINE : {ENG_NAME}")


def serve():
    # uvicorn.run("main:app", host="0.0.0.0", port=10501, reload=True)
    uvicorn.run(app, host="0.0.0.0", port=230806, access_log=True)


ENG_NAME = "fastApiServer"


API_VERSION = f'{ENG_NAME.upper()} ENGINE version 6.0.0'


if __name__ == "__main__":
    rootDir = None # os.environ["API_ROOT"]
    if not rootDir:
        rootDir = os.environ["HOME"]
    configFile = rootDir + './config/api.cfg'
   
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", action="version", version='0.0.1')
    parser.add_argument("--config", type=str, help="컨피그 파일 세팅 위치", default=configFile)


    argument, unknown = parser.parse_known_args()

   
    logWriter.setLogLevel("DEBUG")
    logWriter.setFile(f"./fastApiServer.log")


    # FastAPI 실행
    serve()



