from dataclasses import asdict
from typing import Optional

import uvicorn
from fastapi import FastAPI, Body, status
from fastapi.responses import JSONResponse

# from app.database.conn import db
# from app.common.config import conf
# from app.routes import index

'''
def create_app():
    """
    앱 함수 실행
    :return:
    """
    # c = conf()
    # application: FastAPI = FastAPI()
    # conf_dict = asdict(c)
    # db.init_app(application, **conf_dict)
    # 데이터 베이스 이니셜라이즈

    # 레디스 이니셜라이즈

    # 미들웨어 정의

    # 라우터 정의
    # application.include_router(index)
    # return application


# app: FastAPI = create_app()
'''
app = FastAPI()


@app.get("/")
async def main():
    content = {"title": "this is main content"}
    return JSONResponse(status_code=status.HTTP_200_OK, content=content)


# Path Parameters 예제
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id == 1:
        val = {"item_id": item_id, "item_name": "testItem"}
        return JSONResponse(status_code=status.HTTP_200_OK, content=val)
    else:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content="Bad Request")

# Query Parameters
@app.get("")

@app.get("/error")
async def error():
    content = {"title": "Error is Occured"}
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=content)

# if __name__ == "__main__":
#    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
