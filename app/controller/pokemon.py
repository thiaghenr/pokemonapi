from fastapi import status, HTTPException
from fastapi.encoders import jsonable_encoder
from typing import List

from pydantic import errors
from models.pokemon import Pokemon as pokemon_model
from models.pokemon_type import PokemonType as pokemon_type_model
from models.pokemon import Pokemon as pokemon_model, PokemonTypeAssociation as pokemon_type_association
from schemas.pokemon import ShowPokemon as show_pokemon_schema
from .utils import get_pokemon_types

def get_pokemon_to_show(pokemon: pokemon_model, pokemon_types: List[pokemon_type_model]) -> show_pokemon_schema:
    pokemon_to_show = show_pokemon_schema(
        name = pokemon.name,
        height = pokemon.height,
        weight = pokemon.weight,
        xp = pokemon.xp,
        types = pokemon_types
    )    
    return pokemon_to_show


def get_pokemon_association(pokemon_id, db):
    return db.query(pokemon_type_association).filter(
                                        pokemon_type_association.pokemon_id == pokemon_id).all()


def get_all(db):
    pokemons = db.query(pokemon_model).all()
    show_pokemons = []
    for pokemon in pokemons:
        to_show = get_pokemon_to_show(pokemon, get_pokemon_types(get_pokemon_association(pokemon.id, db), db))
        show_pokemons.append(to_show)
    return show_pokemons


def get_pokemon(pokemon_id, db):
    try:
        pokemon = db.query(pokemon_model).filter(pokemon_model.id == pokemon_id).first()
        if not pokemon:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'Pokemon with the id {pokemon_id} was not found')

        
        pokemon_association = get_pokemon_association(pokemon_id, db)
        pokemon_types = get_pokemon_types(pokemon_association, db)
        
        return get_pokemon_to_show(pokemon, pokemon_types)
    except:
        print('Check if the pokemon exists on the database')


def update_pokemon(pokemon_id, pokemon, db):
    try:
        pokemon_query = db.query(pokemon_model).filter(pokemon_model.id == pokemon_id)
        if not pokemon_query.first():
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'Pokemon with the id {pokemon_id} was not found')
        pokemon = jsonable_encoder(pokemon)
        pokemon_query.update(pokemon)
        db.commit()
    except:
        print('Please check your data')
    

def delete_pokemon(pokemon_id, db):
    try:
        pokemon_query = db.query(pokemon_model).filter(pokemon_model.id == pokemon_id)
        if not pokemon_query.first():
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                                detail = f'Pokemon with the id {pokemon_id} was not found')
        pokemon_query.delete(synchronize_session = False)
        db.commit()
        return jsonable_encoder({'pokemon': 'deleted'})
    except:
        print('Please check your data.')


def create_pokemon(pokemon, db):
    try:
        pkm_types = []
        for tp in pokemon.types:
            pkm_type = db.query(pokemon_type_model).filter(
                pokemon_type_model.name == tp.name).first()
            association = pokemon_type_association(pokemontype_id=pkm_type.id)
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
    
    except Exception as error:
        print('errrr')
        print(error)
        print("Please check the data that you sent.")