from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.encoders import jsonable_encoder
from typing import List
from database import get_db
from models.pokemon import Pokemon as pokemon_model, PokemonTypeAssociation
from models.pokemon_type import PokemonType as pokemon_type_model
from schemas.pokemon import Pokemon as pokemon_schema
from schemas.pokemon import ShowPokemon as show_pokemon_schema

from sqlalchemy.orm import Session

router = APIRouter()


def get_pokemon_to_show(pokemon: pokemon_model, pokemon_types: List[pokemon_type_model]) -> show_pokemon_schema:
    pokemon_to_show = show_pokemon_schema

    pokemon_to_show.name   = pokemon.name
    pokemon_to_show.height = pokemon.height
    pokemon_to_show.weight = pokemon.weight
    pokemon_to_show.xp     = pokemon.xp
    pokemon_to_show.types  = pokemon_types    
    
    return pokemon_to_show


# def get_pokemon_types(pokemon_association, db):
#     return [get_pokemon_type(tp_id.pokemontype_id, db)
#                         for tp_id in pokemon_association]


# def get_pokemon_association(pokemon_id, db):
#     return db.query(models.PokemonAssociation).filter(
#                                         models.PokemonAssociation.pokemon_id == pokemon_id).all()


@router.post('/pokemon', status_code = status.HTTP_201_CREATED, tags = ['Pokemons'])
def create_pokemon(pokemon: pokemon_schema, db: Session = Depends(get_db)):
    pkm_types = []
    
    for tp in pokemon.types:
        pkm_type = db.query(pokemon_type_model).filter(
            pokemon_type_model.name == tp.name).first()

        association = PokemonTypeAssociation(pokemontype_id=pkm_type.id)
        pkm_types.append(association)

    new_pokemon = pokemon_model(
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


@router.delete('/pokemon/{pokemon_id}', status_code = status.HTTP_204_NO_CONTENT, tags = ['Pokemons'])
def delete_pokemon(pokemon_id, db: Session = Depends(get_db)):
    pokemon_query = db.query(pokemon_model).filter(pokemon_model.id == pokemon_id)
    if not pokemon_query.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail = f'Pokemon with the id {pokemon_id} was not found')
    pokemon_query.delete(synchronize_session = False)
    db.commit()

    return 'Deleted'


@router.put('/pokemon/{pokemon_id}', status_code = status.HTTP_202_ACCEPTED, tags = ['Pokemons'])
def update_pokemon(pokemon_id, pokemon: pokemon_schema, db: Session = Depends(get_db)):
    pokemon_query = db.query(pokemon_model).filter(pokemon_model.id == pokemon_id)
    if not pokemon_query.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'Pokemon with the id {pokemon_id} was not found')
    pokemon = jsonable_encoder(pokemon)
    pokemon_query.update(pokemon)
    db.commit()
    return 'Updated'


@router.get('/pokemon', response_model = List[pokemon_schema], tags = ['Pokemons'])
def get_all(db: Session = Depends(get_db)):
    pokemons = db.query(pokemon_model).all()

    show_pokemons = [
        get_pokemon_to_show(pokemon, get_pokemon_types(get_pokemon_association(pokemon.id, db), db))
        for pokemon in pokemons
    ]
    return show_pokemons