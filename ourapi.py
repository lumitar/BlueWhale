from fastapi import FastAPI
from sqlalchemy import *
from sqlalchemy.orm import *
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()
allowed = {"points", "animals"} #если изменится список таблиц, изменить и это!

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

engine = create_engine("sqlite:///data.db",connect_args={"check_same_thread": False},)

@app.get("/points/{id}")
def get_pointsID(id:int):
    with engine.connect() as conn:
        row = conn.execute(text("SELECT * FROM points WHERE id = :id"), {"id": id},).mappings().first()

    if row is None:
        return "Ошибка"
    else:
        return row

@app.get("/animals/id/{id}")
def get_animalID(id:int):
    with engine.connect() as conn:
        row = conn.execute(text("SELECT * FROM animals WHERE id = :id"), {"id": id},).mappings().first()

    if row is None:
        return "Ошибка"
    else:
        return row

@app.get("/animals/group/{namegroup}")
def get_animalGroup(namegroup:str):
    with engine.connect() as conn:
        row = conn.execute(text("SELECT * FROM animals WHERE group_Name = :namegroup"), {"namegroup": namegroup},).mappings().all()
        return row

@app.get("/getTable/{TableName}")
def get_Table(TableName: str):
    if TableName not in allowed:
        return "Ошибка"
    
    with engine.connect() as conn:
        row = conn.execute(text(f"SELECT * FROM {TableName}")).mappings().all()
    return row