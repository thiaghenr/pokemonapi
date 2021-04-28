from typing import List, Optional

from fastapi import FastAPI, Depends, status, Response, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import  BaseModel
from database import engine, SessionLocal
from sqlalchemy.orm import Session
# from . import models, schemas
import models, schemas
# do not forget it
# https://docs.python.org/3/library/http.html#http.HTTPStatus

app = FastAPI()


models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.post('/pokemon', status_code = status.HTTP_201_CREATED)
def create_pokemon(pokemon: schemas.Pokemon, db: Session = Depends(get_db)):
    new_pokemon = models.Pokemon(
        name    = pokemon.name  ,
        height  = pokemon.height,
        weight  = pokemon.weight,
        xp      = pokemon.xp    ,
        image   = pokemon.image
    ) 
    db.add(new_pokemon)
    db.commit()
    db.refresh(new_pokemon)
    print('new_pokemon')
    print(new_pokemon)
    print(type(new_pokemon))
    return new_pokemon


@app.delete('/pokemon/{pokemon_id}', status_code = status.HTTP_204_NO_CONTENT)
def delete_pokemon(pokemon_id, db: Session = Depends(get_db)):
    pokemon_query = db.query(models.Pokemon).filter(models.Pokemon.id == pokemon_id)
    if not pokemon_query.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail = f'Pokemon with the id {pokemon_id} was not found')
    pokemon_query.delete(synchronize_session = False)
    db.commit()

    return 'Deleted'


@app.put('/pokemon/{pokemon_id}', status_code = status.HTTP_202_ACCEPTED)
def update_pokemon(pokemon_id, pokemon: schemas.Pokemon, db: Session = Depends(get_db)):
    pokemon_query = db.query(models.Pokemon).filter(models.Pokemon.id == pokemon_id)
    if not pokemon_query.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'Pokemon with the id {pokemon_id} was not found')
    pokemon = jsonable_encoder(pokemon)
    pokemon_query.update(pokemon)
    db.commit()
    return 'Updated'


@app.get('/pokemon', response_model = List[schemas.ShowPokemon])
def get_all(db: Session = Depends(get_db)):
    pokemons = db.query(models.Pokemon).all()
    return pokemons


@app.get('/pokemon/{pokemon_id}', status_code = status.HTTP_200_OK, response_model = schemas.ShowPokemon)
def get_pokemon(pokemon_id, db: Session = Depends(get_db)):
    pokemon = db.query(models.Pokemon).filter(models.Pokemon.id == pokemon_id).first()
    if not pokemon:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'Pokemon with the id {pokemon_id} was not found')
    return pokemon


@app.post('/pokemonType', status_code = status.HTTP_201_CREATED)
def create_pokemon_type(pokemon_type: schemas.PokemonType, db: Session = Depends(get_db)):
    new_pokemon_type = models.PokemonType(
        name = pokemon_type.name
    )
    db.add(new_pokemon_type)
    db.commit()
    db.refresh(new_pokemon_type)
    return new_pokemon_type


@app.delete('/pokemonType/{type_id}', status_code = status.HTTP_204_NO_CONTENT)
def delete_pokemon_type(type_id, db: Session = Depends(get_db)):
    type_query = db.query(models.PokemonType).filter(models.PokemonType.id == type_id)
    if not type_query.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail = f'The Pokemon Type with the id {type_id} was not found')
    type_query.delete(synchronize_session = False)
    db.commit()

    return 'Deleted'


@app.put('/pokemonType/{type_id}', status_code = status.HTTP_202_ACCEPTED)
def update_pokemon_type(type_id, pokemon_type: schemas.PokemonType, db: Session = Depends(get_db)):
    type_query = db.query(models.PokemonType).filter(models.PokemonType.id == type_id)
    if not type_query.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail = f'The Pokemon Type with the id {type_id} was not found')
    pokemon_type = jsonable_encoder(pokemon_type)
    type_query.update(pokemon_type)
    db.commit()

    return 'Updated'


@app.get('/pokemonType', status_code = status.HTTP_200_OK)
def get_all_pokemon_types(db: Session = Depends(get_db)):
    return db.query(models.PokemonType).all()


@app.post('/user', status_code = status.HTTP_201_CREATED)
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(
        name    = user.name  ,
        email  = user.email,
        password  = user.password
    ) 
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    print('new_user')
    print(new_user)
    print(type(new_user))
    return new_user