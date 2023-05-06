# Create Fast API app

## Create an item class with user's requirements
# Example:
# class Item(BaseModel):
#     year: str
#     product: str
#     sentiment: Optional[str, bool] = None

## Create a Fast API app
# Example:
# app = FastAPI()

## Create a path operation decorator with the path and method
# Example:
# @app.post("/items/")
# def fetch_item(item: Item):
    # create/select the query based on the user's requirements

    # fetch the dataframe using the query

    # convert dataframe to json/dictionary
    # output_dict = df.to_dict()
#     return output_dict

# Run the app
# if __name__ == "__main__":
#     uvicorn.run(app, host="localhost", port=8000)

# Hit 127.0.0.1:8000/items/ in the browser/postman to send the request as a user


