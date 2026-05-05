from fastapi import FastAPI
from datetime import datetime
import time
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

app = FastAPI(
    title="My API",
    description="This is a sample API built with FastAPI",
    version="1.0.0",
)

@app.get("/")
def read_root():
    return {"hello":"world"}

@app.get("/get_time")
def read_server_time():
    return {"server_time": datetime.now().isoformat()}

@app.get("/items/{item_id}")
def get_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

@app.get("/v1/items/{item_id}")
def get_item_v1(item_id: int):
    time.sleep(10)  # Simulate a delay
    return {"item_id": item_id, "version": "v1"}

@app.post("/v1/items/")
def create_items(item: Item):
    return {"name": item.name, "description": item.description, "price": item.price, "tax": item.tax }

@app.put("/v1/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_id": item_id, "name": item.name, "description": item.description, "price": item.price, "tax": item.tax}

@app.delete("/v1/items/{item_id}")
def delete_item(item_id: int):
    return {"item_id": item_id, "status": "deleted"}