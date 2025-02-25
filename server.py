from fastapi import BackgroundTasks, FastAPI
from pydantic import BaseModel
from state import order_items
import main

app = FastAPI()

class Items(BaseModel):
    items: list[str]

@app.post("/run")
def run(items: Items, tasks: BackgroundTasks):
    order_items.extend(items.items)
    
    tasks.add_task(main.task)
    return {"message": "success"}