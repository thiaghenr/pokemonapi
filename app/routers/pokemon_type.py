from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.encoders import jsonable_encoder
from database import get_db
from models.pokemon_type import PokemonType as pokemon_type_model
from schemas.pokemon_type import ShowPokemonType as show_pokemon_type_schema
from schemas.pokemon_type import PokemonType as pokemon_type_schema

from sqlalchemy.orm import Session


router = APIRouter()

@router.post('/pokemonType', status_code = status.HTTP_201_CREATED, tags = ['Pokemon Types'])
def create_pokemon_type(pokemon_type: pokemon_type_schema, db: Session = Depends(get_db)):
    new_pokemon_type = pokemon_type_model(
        name = pokemon_type.name
    )
    db.add(new_pokemon_type)
    db.commit()
    db.refresh(new_pokemon_type)
    return new_pokemon_type


@router.delete('/pokemonType/{type_id}', status_code = status.HTTP_204_NO_CONTENT, tags = ['Pokemon Types'])
def delete_pokemon_type(type_id, db: Session = Depends(get_db)):
    type_query = db.query(pokemon_type_model).filter(pokemon_type_model.id == type_id)
    if not type_query.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail = f'The Pokemon Type with the id {type_id} was not found')
    type_query.delete(synchronize_session = False)
    db.commit()

    return 'Deleted'


@router.put('/pokemonType/{type_id}', status_code = status.HTTP_202_ACCEPTED, tags = ['Pokemon Types'])
def update_pokemon_type(type_id, pokemon_type: pokemon_type_schema, db: Session = Depends(get_db)):
    type_query = db.query(pokemon_type_model).filter(pokemon_type_model.id == type_id)
    if not type_query.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail = f'The Pokemon Type with the id {type_id} was not found')
    pokemon_type = jsonable_encoder(pokemon_type)
    type_query.update(pokemon_type)
    db.commit()

    return 'Updated'


@router.get('/pokemonType/{pokemon_type_id}', status_code = status.HTTP_200_OK, response_model = show_pokemon_type_schema, tags = ['Pokemon Types'])
def get_pokemon_type(pokemon_type_id, db: Session = Depends(get_db)):
    pokemon_type = db.query(pokemon_type_model).filter(pokemon_type_model.id == pokemon_type_id).first()
    if not pokemon_type:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'The Pokemon Type with the id {pokemon_type_id} was not found!')
    return pokemon_type


@router.get('/pokemonType', status_code = status.HTTP_200_OK, tags = ['Pokemon Types'])
def get_all_pokemon_types(db: Session = Depends(get_db)):
    return db.query(pokemon_type_model).all()