from fastapi import APIRouter, Depends, status
from typing import List
from database import get_db
from schemas.pokemon import Pokemon as pokemon_schema
from controller import pokemon as pkm_controller
from schemas.pokemon import ShowPokemon as show_pokemon_schema
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/pokemon',
    tags = ['Pokemons']
)


@router.post('', status_code = status.HTTP_201_CREATED)
def create_pokemon(pokemon: pokemon_schema, db: Session = Depends(get_db)):
    new_pokemon = pkm_controller.create_pokemon(pokemon, db)
    return new_pokemon


@router.delete('/{pokemon_id}', status_code = status.HTTP_204_NO_CONTENT)
def delete_pokemon(pokemon_id, db: Session = Depends(get_db)):
    pkm_controller.delete_pokemon(pokemon_id, db)
    return 'Deleted'


@router.put('/{pokemon_id}', status_code = status.HTTP_202_ACCEPTED)
def update_pokemon(pokemon_id, pokemon: pokemon_schema, db: Session = Depends(get_db)):
    pkm_controller.update_pokemon(pokemon_id, pokemon, db)
    return 'Updated'


@router.get('/{pokemon_id}', status_code = status.HTTP_200_OK, response_model = show_pokemon_schema)
def get_pokemon(pokemon_id, db: Session = Depends(get_db)):
    return pkm_controller.get_pokemon(pokemon_id, db)


@router.get('', response_model = List[show_pokemon_schema])
def get_all(db: Session = Depends(get_db)):
    return pkm_controller.get_all(db)