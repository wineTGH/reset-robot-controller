from fastapi import BackgroundTasks, FastAPI
from pydantic import BaseModel
import main

app = FastAPI()

class Items(BaseModel):
    items: list[str]

@app.post("/run")
def run(items: Items, tasks: BackgroundTasks):
    tasks.add_task(main.task, items.items)
    return {"message": "success"}