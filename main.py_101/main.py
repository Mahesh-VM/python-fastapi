from fastapi import FastAPI
from datetime import datetime
import time

app = FastAPI()

@app.get("/")
def read_root():
    return {"hello":"world"}

@app.get("/get_time")
def read_server_time():
    return {"server_time": datetime.now().isoformat()}

@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {"item_id": item_id}

@app.get("/v1/items/{item_id}")
def get_item_v1(item_id: int):
    time.sleep(10)  # Simulate a delay
    return {"item_id": item_id, "version": "v1"}