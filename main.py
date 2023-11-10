from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()



class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]

@app.get("/")

async def root():
    return {"message": "start"}

@app.post("/post")
async def post() -> dict:
    return post_db.dict()

#@app.get("/dog",  response_model=list[Dog], summary='Get Dogs')
@app.get("/dog")
async def dog() -> list:
    return DogType._member_names_

@app.post("/dog")
async def dog(item: Dog):
    return item.dict()

@app.get("/dog/{pk}")
async def pk(pk: int) -> dict:
    return dogs_db[pk].dict()

@app.patch("/dog/{pk}")
async def dog_pk(pk: int, item: Dog):
    Dog_in_db = dogs_db[pk]
    Dog_update = Dog(**Dog_in_db)
    update_data = item.dict(exclude_unset=True)
    updated_item = Dog_update.copy(update=update_data)
    return updated_item

