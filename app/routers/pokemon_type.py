from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.encoders import jsonable_encoder
from database import get_db
from models.pokemon_type import PokemonType as pokemon_type_model
from schemas.pokemon_type import ShowPokemonType as show_pokemon_type_schema
from schemas.pokemon_type import PokemonType as pokemon_type_schema
from controller import pokemon_type as pkm_type_controller
from sqlalchemy.orm import Session


router = APIRouter(
    prefix='/pokemonType',
    tags = ['Pokemon Types']
)

@router.post('', status_code = status.HTTP_201_CREATED)
def create_pokemon_type(pokemon_type: pokemon_type_schema, db: Session = Depends(get_db)):
    new_pokemon_type = pkm_type_controller.create(pokemon_type, db)
    return new_pokemon_type


@router.delete('/{type_id}', status_code = status.HTTP_204_NO_CONTENT)
def delete_pokemon_type(type_id, db: Session = Depends(get_db)):
    pkm_type_controller.delete(type_id, db)
    return 'Deleted'


@router.put('/{type_id}', status_code = status.HTTP_202_ACCEPTED)
def update_pokemon_type(type_id, pokemon_type: pokemon_type_schema, db: Session = Depends(get_db)):
    pkm_type_controller.update(type_id, pokemon_type, db)
    return 'Updated'


@router.get('/{pokemon_type_id}', status_code = status.HTTP_200_OK, response_model = show_pokemon_type_schema)
def get_pokemon_type(pokemon_type_id, db: Session = Depends(get_db)):
    pokemon_type = pkm_type_controller.get(pokemon_type_id, db)
    return pokemon_type


@router.get('', status_code = status.HTTP_200_OK)
def get_all_pokemon_types(db: Session = Depends(get_db)):
    return db.query(pokemon_type_model).all()