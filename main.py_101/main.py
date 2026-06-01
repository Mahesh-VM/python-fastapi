from fastapi import FastAPI, Query, Path
from datetime import datetime
import time, random
from pydantic import BaseModel, AfterValidator
from typing import Annotated

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

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

"""
usage for query parameters with validation:
using Annotated from typing and Query from fastapi, we can add validation rules to query parameters. In this example, the 
query parameter 'q' is optional and has a maximum length of 50 characters. If the client sends a query parameter that 
exceeds this length, FastAPI will automatically return a validation error response.
could also add other validation rules such as min_length, regex, etc. to further validate the input.
"""
@app.get("/v1/items")
def read_items(q: Annotated[str | None, Query(min_length=4, max_length=50, pattern="^freeWorld$")] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# read mulitple items with query parameters
@app.get("/v1/read/multiple/items")
def read_multiple_items(
    q: Annotated[list[str] | None, 
                 Query(
                     title="Search Query", 
                     description="A list of search queries"
                     )] = None
    ):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

data = {
    "imdb-jkd783nd8hsn": "The Shawshank Redemption",
    "imdb-jsdfkj992hsn": "The Godfather",
    "imdb-ooapml92kla1": "The Dark Knight",
    "isbn-978-3-16-148410-0": "The Great Gatsby",
    "isbn-978-0-14-028333-4": "To Kill a Mockingbird",
    "isbn-978-0-452-28423-4": "1984",
    "uasdo19nd933n": "Unknown Item"
}

def check_valid_id(item_id: str):
    if not item_id.startswith(("imdb-", "isbn-")):
        raise ValueError("Invalid item ID format. Must start with 'imdb-' or 'isbn-'.")
    return item_id

@app.get("/v1/items/read/")
async def read_items(
    id: Annotated[str | None, 
        Query(
            description="The ID of the item to retrieve", 
            example="imdb-jkd783nd8hsn", 
            min_length=10, 
            max_length=30, 
            regex="^(imdb-|isbn-).+$", 
            alias="item_id"),
            AfterValidator(check_valid_id)] = None
):
    if id:
        item = data.get(id)
    else:
        id, item = random.choice(list(data.items()))
    return {"item_id": id, "item": item}
    

@app.get("/v1/get-item/{item_id}")
async def get_item_by_id(
    item_id: Annotated[int, Path(title="Item ID", description="The ID of the item to retrieve", ge=1, le=1000)],
    q: Annotated[str | None, Query(alias="item-query")] = None,
    ):
    results = {"item_id": item_id}
    print(q)
    if q:
        print(q)
        results.update({"q":q})
    return results

@app.post("/v1/items/")
def create_items(item: Item):
    # return {"name": item.name, "description": item.description, "price": item.price, "tax": item.tax }
    item_dict = item.model_dump()
    if item.tax is not None:
        total_price = item.price + item.tax
        item_dict.update({"total_price": total_price})
    return item_dict

@app.put("/v1/items/{item_id}")
def update_item(item_id: int, item: Item):
    # return {"item_id": item_id, "name": item.name, "description": item.description, "price": item.price, "tax": item.tax}
    if item.tax is not None:
        total_price = item.price + item.tax
        item_dict = item.model_dump()
        item_dict.update({"total_price": total_price})
    return {"item_id": item_id, **item_dict}

@app.delete("/v1/items/{item_id}")
def delete_item(item_id: int):
    return {"item_id": item_id, "status": "deleted"}