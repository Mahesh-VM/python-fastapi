from fastapi import FastAPI
import httpx

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    async with httpx.AsyncClient(timeout=12) as client:
        response = await client.get(f"http://127.0.0.1:8000/v1/items/{item_id}")
        data = response.json()
    return {"item_id": item_id, "data": data}