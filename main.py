#Kallya Ellen R. da Silva - TDS(326)

from fastapi import FastAPI, HTTPException, Query, Path, status
from typing import List, Optional
from pydantic import BaseModel
from uuid import uuid4
from datetime import datetime

# ---------modelos -------------#
class FlowerCreate(BaseModel):
    name: str
    color: str
    type: Optional[str] = None  
    blooming: bool = False  

class Flower(FlowerCreate):
    id: str
    planted_at: datetime

app = FastAPI(title="API de Flores", version="1.0")

# db para as flores
flowers_db = {}

# ----------função p popular flores------------#

def populate_flowers_db():
    initial_flowers = [
        {"name": "Rosa", "color": "Vermelha", "type": "Ornamental", "blooming": True},
        {"name": "Girassol", "color": "Amarelo", "type": "Ornamental", "blooming": True},
        {"name": "Lavanda", "color": "Roxa", "type": "Aromática", "blooming": False}
    ]
    for flower in initial_flowers:
        flower_id = str(uuid4())
        new_flower = Flower(id=flower_id, planted_at=datetime.utcnow(), **flower)
        flowers_db[flower_id] = new_flower

# niciar a aplicação
@app.on_event("startup")
def startup_event():
    populate_flowers_db()
# obs: 'startup' evento para inciar uma aplicação

# ----------- endpoints -----------

#criar flor
@app.post("/flowers", response_model=Flower, status_code=status.HTTP_201_CREATED)
def create_flower(flower: FlowerCreate):
    flower_id = str(uuid4())
    new_flower = Flower(id=flower_id, planted_at=datetime.utcnow(), **flower.dict())
    flowers_db[flower_id] = new_flower
    return new_flower

# lista de flores
@app.get("/flowers", response_model=List[Flower], status_code=status.HTTP_200_OK)
def list_flowers(skip: int = Query(0, ge=0), limit: int = Query(10, gt=0)):
    return list(flowers_db.values())[skip : skip + limit]

# buscar flor pelo id 
@app.get("/flowers/{flower_id}", response_model=Flower, status_code=status.HTTP_200_OK)
def get_flower(flower_id: str = Path(...)):
    flower = flowers_db.get(flower_id)
    if not flower:
        raise HTTPException(status_code=404, detail="Flor não encontrada")
    return flower

# atualizar flor
@app.put("/flowers/{flower_id}", response_model=Flower, status_code=status.HTTP_200_OK)
def update_flower(flower_id: str, flower: FlowerCreate):
    stored_flower = flowers_db.get(flower_id)
    if not stored_flower:
        raise HTTPException(status_code=404, detail="Flor não encontrada")
    updated_flower = Flower(id=flower_id, planted_at=stored_flower.planted_at, **flower.dict())
    flowers_db[flower_id] = updated_flower
    return updated_flower

# deletar flor
@app.delete("/flowers/{flower_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_flower(flower_id: str):
    if flower_id in flowers_db:
        del flowers_db[flower_id]
    else:
        raise HTTPException(status_code=404, detail="Flor não encontrada")
