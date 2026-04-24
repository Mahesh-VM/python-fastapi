from fastapi import FastAPI
from datetime import datetime

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