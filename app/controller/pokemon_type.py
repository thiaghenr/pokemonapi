from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.encoders import jsonable_encoder
from database import get_db
from models.pokemon_type import PokemonType as pokemon_type_model
from schemas.pokemon_type import ShowPokemonType as show_pokemon_type_schema
from schemas.pokemon_type import PokemonType as pokemon_type_schema

from sqlalchemy.orm import Session



def create(pokemon_type, db):
    new_pokemon_type = pokemon_type_model(
        name = pokemon_type.name
    )
    db.add(new_pokemon_type)
    db.commit()
    db.refresh(new_pokemon_type)
    return new_pokemon_type


def delete(type_id, db):
    type_query = db.query(pokemon_type_model).filter(pokemon_type_model.id == type_id)
    if not type_query.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail = f'The Pokemon Type with the id {type_id} was not found')
    type_query.delete(synchronize_session = False)
    db.commit()


def update(type_id, pokemon_type, db):
    type_query = db.query(pokemon_type_model).filter(pokemon_type_model.id == type_id)
    if not type_query.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail = f'The Pokemon Type with the id {type_id} was not found')
    pokemon_type = jsonable_encoder(pokemon_type)
    type_query.update(pokemon_type)
    db.commit()


def get(pokemon_type_id, db):
    pokemon_type = db.query(pokemon_type_model).filter(pokemon_type_model.id == pokemon_type_id).first()
    if not pokemon_type:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'The Pokemon Type with the id {pokemon_type_id} was not found!')
    return pokemon_type