from fastapi import FastAPI
from db import ConnectDB
from model import Trade

app = FastAPI()

@app.get('/trades')
def get_trades_list() -> list[Trade]:
    db = ConnectDB()
    collection = db.get_collection()
    cursor = collection.find()
    print(len(cursor))