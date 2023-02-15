from fastapi  import FastAPI
import uvicorn
from pydantic import BaseModel

class Item(BaseModel):
    user_id: str
    index: int

database = ['Car', 'Bike', 'Bus']

user_id = "ABC123"

app = FastAPI()


@app.get("/")
def getinfo():
    return {"Result": "Hello World.. Chacko.. how do you do...."}

@app.post("/user_item")
def fetch_item(user_item: Item):
    if user_item['user_id'] == user_id:
        response_item = database[user_item['index']]
    return {"Response is: ": response_item}
