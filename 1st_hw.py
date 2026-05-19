import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class PetCreateSchema(BaseModel):
    category: str
    title: str

class PetSchema(BaseModel):
    identifier: int
    category: str
    title: str

@app.post("/animals")
def add_new_pet(body: PetCreateSchema) -> PetSchema:
    return PetSchema(identifier=1, category=body.category, title=body.title)

@app.get("/animals/{item_id}")
def fetch_single_pet(item_id: int) -> PetSchema:
    return PetSchema(identifier=1, category="cat", title="Мурзик")

@app.put("/animals/{item_id}")
def modify_existing_pet(item_id: int, payload: PetCreateSchema):
    updated_record = PetSchema(identifier=item_id, category=payload.category, title=payload.title)
    return updated_record

@app.delete("/animals/{item_id}")
def remove_pet(item_id: int):
    pass

if __name__ == "__main__":
    uvicorn.run(app)
