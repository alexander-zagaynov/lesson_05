from fastapi import FastAPI, Request
import logging
from typing import Optional
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
templates = Jinja2Templates(directory='./lesson05/templates')


app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


@app.get('/HW/')
async def read_root():
    logger.info('Отработал GET запрос')
    return {"Hello": "World"}


@app.post("/items_crt/")
async def create_item(item: Item):
    logger.info('Отработал POST запрос.')
    return item


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    logger.info(f'Отработал PUT запрос для item id = {item_id}.')
    return {"item_id": item_id, "item": item}


@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    logger.info(f'Отработал DELETE запрос для item id = {item_id}.')
    return {"item_id": item_id}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}


@app.get("/users/{user_id}/orders/{order_id}")
async def read_data(user_id: int, order_id: int):
    # обработка данных
    return {"user_id": user_id, "order_id": order_id}


@app.get("/items_sl/")
async def skip_limit(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}


@app.get("/", response_class=HTMLResponse)
async def read_root():
    return "<h1>Hello World</h1>"


@app.get("/message")
async def read_message():
    message = {"message": "Hello World"}
    return JSONResponse(content=message, status_code=200)


@app.get("/{name}", response_class=HTMLResponse)
async def read_item(request: Request, name: str):
    return templates.TemplateResponse("item.html", {"request": request, "name": name})

"""
Интерактивная документация
 
Swagger — инструмент для создания и документирования API. FastAPI
использует Swagger UI для генерации интерактивной документации, которая
отображает все маршруты, параметры и модели данных, которые были определены
в приложении.
Для просмотра интерактивной документации Swagger нужно запустить приложение
и перейти по адресу http://localhost:8000/docs. 

ReDoc — альтернативный инструмент для документирования API, который
также поддерживается FastAPI. Он предоставляет более простой и лаконичный
интерфейс для просмотра документации.
Для просмотра документации ReDoc нужно запустить приложение и перейти по
адресу http://localhost:8000/redoc.

"""