import json
from fastapi import Depends
from sqlalchemy.orm import Session

import sqlite3





def add_pokemon(db: Session = Depends(get_db)):
    with open('Pokemon.json', 'r') as pokemons:
        pokemons = json.load(pokemons)

    for pokemon in pokemons['pokemon']:
        print("==========")
        print(pokemon)

if __name__ == '__main__':
    ee = 'hello world aa'
    ee = ('').join(ee)
    print(ee)
    add_pokemon()