from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from typing import List

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
    0: Dog(name="Bob", pk=0, kind="terrier"),
    1: Dog(name="Marli", pk=1, kind="bulldog"),
    2: Dog(name="Snoopy", pk=2, kind="dalmatian"),
    3: Dog(name="Rex", pk=3, kind="dalmatian"),
    4: Dog(name="Pongo", pk=4, kind="dalmatian"),
    5: Dog(name="Tillman", pk=5, kind="bulldog"),
    6: Dog(name="Uga", pk=6, kind="bulldog"),
}

post_db = [Timestamp(id=0, timestamp=12), Timestamp(id=1, timestamp=10)]


@app.get("/")
async def root():
    return {"message": "start"}


@app.post("/post", summary="Get Post")
async def post() -> Timestamp:
    new_timestamp = datetime.now()
    post_timestamp = int(round(new_timestamp.timestamp()))
    last_id = len(post_db)
    post_db.append(Timestamp(id=last_id, timestamp=post_timestamp))
    return post_db[-1]

@app.get("/dog", response_model=List[Dog], summary="Get Dogs")
async def dog(kind: DogType = None) -> List[Dog]:
    if kind is None:
        dog_list = dogs_db.values()
    else:
        dog_list = [
            dog_in_db for dog_in_db in dogs_db.values() if dog_in_db.kind == kind
        ]
    return dog_list


@app.post("/dog", response_model=Dog, summary="Create Dog")
async def get_dogs(item: Dog) -> Dog:
    last_value = List(dogs_db)[-1] + 1
    dogs_db[last_value] = item
    return dogs_db[last_value]


@app.get("/dog/{pk}", response_model=Dog, summary="Get Dog By Pk")
async def pk(pk: int) -> Dog:
    return dogs_db[pk]

@app.patch("/dog/{pk}", response_model=Dog, summary="Update Dog")
async def dog_pk(pk: int, item: Dog) -> Dog:
    dog_in_db = dogs_db[pk]
    dog_in_db.name = item.name
    dog_in_db.kind = item.kind
    return dog_in_db

