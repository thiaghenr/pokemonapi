import json

from database import engine, SessionLocal
from sqlalchemy.orm import Session
from models.pokemon import Pokemon

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()



def add_pokemon():
    with open('../Pokemon.json', 'r') as pokemons:
        pokemons = json.load(pokemons)
    db = SessionLocal()
    for pokemon in pokemons['pokemon']:
        new_pokemon = Pokemon(
            name    = pokemon['name']   ,
            height  = pokemon['height'] ,
            weight  = pokemon['weight'] ,
            xp      = pokemon['xp']     ,
            image   = pokemon['image']
        ) 
        db.add(new_pokemon)
    db.commit()

if __name__ == '__main__':
    ee = 'hello world aa'
    ee = ('').join(ee)
    print(ee)
    add_pokemon()