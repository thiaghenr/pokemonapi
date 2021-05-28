from logging import exception
from typing import List, Optional

from fastapi import FastAPI, Depends, responses, status, Response, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import  BaseModel
from database import engine, SessionLocal
from sqlalchemy.orm import Session

# from . import models, schemas
import models, schemas, hashing
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


@app.post('/pokemon', status_code = status.HTTP_201_CREATED, tags = ['Pokemons'])
def create_pokemon(pokemon: schemas.Pokemon, db: Session = Depends(get_db)):
    pkm_types = []
    
    for tp in pokemon.types:
        pkm_type = db.query(models.PokemonType).filter(
            models.PokemonType.name == tp.name).first()

        association = models.PokemonAssociation(pokemontype_id=pkm_type.id)
        pkm_types.append(association)

    new_pokemon = models.Pokemon(
        name    = pokemon.name  ,
        height  = pokemon.height,
        weight  = pokemon.weight,
        xp      = pokemon.xp    ,
        types   = pkm_types ,
        image   = pokemon.image
    ) 
    
    db.add(new_pokemon)
    db.commit()
    db.refresh(new_pokemon)
    
    return new_pokemon


@app.delete('/pokemon/{pokemon_id}', status_code = status.HTTP_204_NO_CONTENT, tags = ['Pokemons'])
def delete_pokemon(pokemon_id, db: Session = Depends(get_db)):
    pokemon_query = db.query(models.Pokemon).filter(models.Pokemon.id == pokemon_id)
    if not pokemon_query.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail = f'Pokemon with the id {pokemon_id} was not found')
    pokemon_query.delete(synchronize_session = False)
    db.commit()

    return 'Deleted'


@app.put('/pokemon/{pokemon_id}', status_code = status.HTTP_202_ACCEPTED, tags = ['Pokemons'])
def update_pokemon(pokemon_id, pokemon: schemas.Pokemon, db: Session = Depends(get_db)):
    pokemon_query = db.query(models.Pokemon).filter(models.Pokemon.id == pokemon_id)
    if not pokemon_query.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'Pokemon with the id {pokemon_id} was not found')
    pokemon = jsonable_encoder(pokemon)
    pokemon_query.update(pokemon)
    db.commit()
    return 'Updated'


@app.get('/pokemon', response_model = List[schemas.ShowPokemon], tags = ['Pokemons'])
def get_all(db: Session = Depends(get_db)):
    pokemons = db.query(models.Pokemon).all()
    return pokemons


@app.get('/pokemon/{pokemon_id}', status_code = status.HTTP_200_OK, response_model = schemas.ShowPokemon, tags = ['Pokemons'])
def get_pokemon(pokemon_id, db: Session = Depends(get_db)):
    pokemon = db.query(models.Pokemon).filter(models.Pokemon.id == pokemon_id).first()
    if not pokemon:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'Pokemon with the id {pokemon_id} was not found')
    print("type(pokemon)")
    print(type(pokemon))
    print("type(pokemon)")
    print("=====")
    print(response_model)
    pkm_type_association = db.query(models.PokemonAssociation).filter(
                                        models.PokemonAssociation.pokemon_id == pokemon_id).all()

    import pprint
    pokemon_types = [{'name': get_first(models.PokemonType, tp_id.pokemontype_id, db).name} 
                        for tp_id in pkm_type_association]
    pokemon['types'] = pokemon_types
    # print(pokemon_types[0].pokemontype_id) 
    # pprint.PrettyPrinter().pprint(pokemon_types[0].name)
    
    return pokemon


@app.post('/pokemonType', status_code = status.HTTP_201_CREATED, tags = ['Pokemon Types'])
def create_pokemon_type(pokemon_type: schemas.PokemonType, db: Session = Depends(get_db)):
    new_pokemon_type = models.PokemonType(
        name = pokemon_type.name
    )
    db.add(new_pokemon_type)
    db.commit()
    db.refresh(new_pokemon_type)
    return new_pokemon_type


@app.delete('/pokemonType/{type_id}', status_code = status.HTTP_204_NO_CONTENT, tags = ['Pokemon Types'])
def delete_pokemon_type(type_id, db: Session = Depends(get_db)):
    type_query = db.query(models.PokemonType).filter(models.PokemonType.id == type_id)
    if not type_query.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail = f'The Pokemon Type with the id {type_id} was not found')
    type_query.delete(synchronize_session = False)
    db.commit()

    return 'Deleted'


@app.put('/pokemonType/{type_id}', status_code = status.HTTP_202_ACCEPTED, tags = ['Pokemon Types'])
def update_pokemon_type(type_id, pokemon_type: schemas.PokemonType, db: Session = Depends(get_db)):
    type_query = db.query(models.PokemonType).filter(models.PokemonType.id == type_id)
    if not type_query.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail = f'The Pokemon Type with the id {type_id} was not found')
    pokemon_type = jsonable_encoder(pokemon_type)
    type_query.update(pokemon_type)
    db.commit()

    return 'Updated'


@app.get('/pokemonType/{pokemon_type_id}', status_code = status.HTTP_200_OK, tags = ['Pokemon Types'])
def get_pokemon_type(pokemon_type_id, db: Session = Depends(get_db)):
    pokemon_type = db.query(models.PokemonType).filter(models.PokemonType.id == pokemon_type_id).first()
    if not pokemon_type:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'The Pokemon Type with the id {pokemon_type_id} was not found!')
    return pokemon_type


@app.get('/pokemonType', status_code = status.HTTP_200_OK, tags = ['Pokemon Types'])
def get_all_pokemon_types(db: Session = Depends(get_db)):
    return db.query(models.PokemonType).all()


@app.post('/user', status_code = status.HTTP_201_CREATED, response_model = schemas.GetUser, tags = ['Users'])
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(
        name    = user.name  ,
        email  = user.email,
        password  = hashing.Hash().bcrypt(user.password)
    ) 
    print('newuser=====')
    print(new_user)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get('/user/{id}', response_model = schemas.GetUser, tags = ['Users'])
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail = f'The User  with the id {user_id} was not found')
    return user


def get_first(table_model, id_table, db):
    return db.query(table_model).filter(table_model.id == id_table).first()