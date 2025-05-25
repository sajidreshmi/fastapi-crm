from fastapi import FastAPI
from typing import List
from pydantic import BaseModel

app = FastAPI()

class Tea(BaseModel):
    id: int
    name: str
    origin: str

teas: List[Tea] = []

@app.get("/")
def read_root():
    return {"msg": "Hello World"}

@app.get("/teas")
def read_teas():
    return teas

@app.get("/teas/{tea_id}")
def read_tea(tea_id: int):
    for tea in teas:
        if tea.id == tea_id:
            return tea
    return {"msg": "Tea not found"}

@app.post("/teas")
def create_tea(tea: Tea):
    teas.append(tea)
    return tea

@app.put("/teas/{tea_id}")
def update_tea(tea_id: int, tea: Tea):
    for i in range(len(teas)):
        if teas[i].id == tea_id:
            teas[i] = tea
            return tea
    return {"msg": "Tea not found"}
    
@app.delete("/teas/{tea_id}")
def delete_tea(tea_id: int):
    for i in range(len(teas)):
        if teas[i].id == tea_id:
            del teas[i]
            return {"msg": "Tea deleted"}
    return {"msg": "Tea not found"}