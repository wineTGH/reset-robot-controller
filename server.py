from fastapi import BackgroundTasks, FastAPI
from pydantic import BaseModel
import state
import main

app = FastAPI()

class Order(BaseModel):
    items: list[str]
    boxes: str

@app.post("/run")
def run(order: Order, tasks: BackgroundTasks):
    # order_items.extend(order.items)
    state.boxes = order.boxes
    
    tasks.add_task(main.task)
    return {"message": "success"}