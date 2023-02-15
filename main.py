from fastapi  import FastAPI
from pydantic import BaseModel

class UserItem(BaseModel):
    user_id: str
    index: int

database = ['Car', 'Bike', 'Bus']

user_id_1 = "ABC123"

app = FastAPI()


@app.get('/')
def getinfo():
    return {"Result": "Hello World.. Chacko.. how do you do...."}

@app.post('/item')
def fetch_item(user_item: UserItem):
    if user_item.user_id == user_id_1:
        idx = user_item.index
        response_item = database[idx]
        return {"Response": response_item}
    else:
        return {"Response": "Invalid user"}
