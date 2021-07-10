# from logging import exception
# from typing import List, Optional

from fastapi import FastAPI#, Depends, responses, status, Response, HTTPException
# from fastapi.encoders import jsonable_encoder
# from pydantic import  BaseModel
from database import engine#, SessionLocal
# from sqlalchemy.orm import Session

from models import pokemon, pokemon_type, team, user
from routers import pokemon as pokemon_router
from routers import pokemon_type as pokemon_type_router

# import models, schemas, hashing
# do not forget it
# https://docs.python.org/3/library/http.html#http.HTTPStatus

app = FastAPI(
    title="Pokemon Project",
    description="Be ready to get your Pokemons",
    version="1.0"
)



pokemon_type.Base.metadata.create_all(engine)
pokemon.Base.metadata.create_all(engine)
user.Base.metadata.create_all(engine)
team.Base.metadata.create_all(engine)


app.include_router(pokemon_router.router)
app.include_router(pokemon_type_router.router)