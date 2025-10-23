from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
#Run program: uvicorn FastAPITutorial:app --reloa
app = FastAPI()
#All json/routes available http://127.0.0.1:8000/openapi.json
#http://127.0.0.1:8000/docs for the docs on FastAPI
class Item(BaseModel):
    text: str
    is_done: bool = False

items = []

@app.get("/")
def root():
    return {"message": "Hello World"}

#Post items Command: curl -X POST -H "Content-Type: application/json" 'http://127.0.0.1:8000/items?item=orange
#Command if items is a JSON Model: curl -X POST -H "Content-Type: application/json" -d '{"text":"apple"}' 'http://127.0.0.1:8000/items'
@app.post("/items")
def create_item(item: Item):
    items.append(item)
    return items

# curl -X GET 'http://127.0.0.1:8000/items?limit=3'
@app.get("/items", response_model=list[Item])
def list_item(limit: int = 10):
    return items[0:limit]
#Get items command: curl -X GET http://127.0.0.1:8000/items/0
#NOTE: Make sure items list is not empty or you will get a Internal Server Error
@app.get("/items/{item_id}", response_model=Item) #Add response_model if Item is a JSON model.
def get_item(item_id: int) -> Item:
    if item_id < len(items):
        item = items[item_id]
        return item
    else:
        raise HTTPException(status_code=404, detail="Item not found")
