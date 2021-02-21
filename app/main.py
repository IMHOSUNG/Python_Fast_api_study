from dataclasses import asdict
from typing import Optional
from fastapi import FastAPI, Body, status, Query, Path
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field  # 파싱을 도와주는 툴일 뿐, Validation Check을 해주는 라이브러리는 아니다.

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
async def parameters_read_item(item_id: int):
    if item_id == 1:
        val = {"item_id": item_id, "item_name": "testItem"}
        return JSONResponse(status_code=status.HTTP_200_OK, content=val)
    else:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content="Bad Request")


# Query Parameters
fake_item_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/query/items/")
async def query_read_item(skip: int = 0, limit: int = 10):
    return fake_item_db[skip: skip + limit]


@app.get("/query/items/{item_id}")
async def query_param_read_item(item_id: str, short: bool = False, skip: int = 0, limit: Optional[str] = None):
    item = {"item_id": item_id}
    if limit:
        item.update(({"limit": limit}))
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


# Request Body

class Item(BaseModel):
    name: str
    description: Optional[str] = Field( #Field 등록을 통해 Swagger에 설명
        None, title="The description of the item", max_length=300
    )
    price: float
    tax: Optional[float] = None


@app.post("/items/")
async def create_item(item: Item):
    return item


# Post vs Put 차이점 ( Post는 무조건 새로 생성, Put은 중복되지 않는 것만 생성 )
@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Item, q: Optional[str] = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result


# Query Parameters and String Validations
@app.get("/items/validations")
async def read_items(q: Optional[str] = Query(None, min_length=3, max_length=50, regex="^fixedquery")):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get("/items/validations/all")
async def read_items(
        q: Optional[str] = Query(
            None,
            alias="item-query",
            title="Query string",
            description="Query string for the items to search in the database that have a good match",
            min_length=3,
            max_length=50,
            regex="^fixedquery$",
            deprecated=True,
        )
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get("/items/")
async def read_items(q: Optional[str] = Query(None, alias="item-query")):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# Path Parameters and Numeric Validations
@app.get("/pathparam/items/{item_id}")
async def read_items(
        *,
        item_id: int = Path(..., title="The ID of the item to get"),
        q: Optional[str] = Query(None, alias="item-query"),
        s: str,
        size: float = Query(..., gt=0, lt=10.5)
):
    results = {"item_id": item_id, "s": s, "size": size}
    if q:
        results.update({"q": q})
    return results


# Body - Multiple Parameter

class User(BaseModel):
    username: str
    full_name: Optional[str] = None


@app.put("/mul/items/{item_id}")
async def update_item(
        *,
        item_id: int,
        item: Item = Body(...,embed=True),
        user: User,
        importance: int = Body(..., gt=0),  # 해당 부분을 통해 Body 값의 Validation 진행
        q: Optional[str] = None
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    if q:
        results.update({"q": q})
    return results


@app.get("/error")
async def error():
    content = {"title": "Error is Occured"}
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=content)

# if __name__ == "__main__":
#    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
