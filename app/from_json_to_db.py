import json

from database import engine, SessionLocal
from sqlalchemy.orm import Session
from models.pokemon import Pokemon, PokemonTypeAssociation
from models.pokemon_type import PokemonType

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def main():
    db = SessionLocal()
    with open('../Pokemon.json', 'r') as pokemons:
        pokemons = json.load(pokemons)
    add_pokemon_types(db, pokemons['pokemon'])
    add_pokemon(db, pokemons['pokemon'])


def add_pokemon_types(db, pokemons):
    try:
        types = []
        for pokemon in pokemons:
            pokemon_types = pokemon['types']
            for pokemon_type in pokemon_types:
                if pokemon_type not in types:
                    types.append(pokemon_type)
        
        for pokemon_type in types:
            new_type = PokemonType(
                name = pokemon_type
            )
            db.add(new_type)
        db.commit()
    except Exception as e:
        print('Please take a look at the function that add the pokemon types to the database...')
        print(e)
        print('==========')
        

def make_pokemon_type_association(db, pokemon_id, pokemon_types):
    try:
        types = db.query(PokemonType).filter(PokemonType.name.in_(pokemon_types)).all()
        for tp in types:
            new_association = PokemonTypeAssociation(
                pokemon_id = pokemon_id,
                pokemontype_id = tp.id
            )
            db.add(new_association)
        db.commit()
    except Exception as e:
        print('Please take a look at the function that make the pokemon association to the database...')
        print(e)
        print('==========')


def add_pokemon(db, pokemons):
    try:
        for pokemon in pokemons:
            new_pokemon = Pokemon(
                id      = pokemon['id'],
                name    = pokemon['name']   ,
                height  = pokemon['height'] ,
                weight  = pokemon['weight'] ,
                xp      = pokemon['xp']     ,
                image   = pokemon['image']
            )
            db.add(new_pokemon)
            make_pokemon_type_association(db, pokemon['id'], pokemon['types'])
        db.commit()
    except Exception as e:
        print('Please take a look at the function that add the pokemon to the database...')
        print(e)
        print('==========')


if __name__ == '__main__':
    main()