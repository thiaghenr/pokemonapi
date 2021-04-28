from pydantic import BaseModel
from typing import List, Optional

#{"id": 1, "name": "bulbasaur", "height": 0.7, "weight": 6.9, "xp": 64, "types": ["poison", "grass"], "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png"}


class PokemonType(BaseModel):
    name: str


class ShowPokemonType():
    name: str
    class Config():
        orm_mode = True




class Pokemon(BaseModel):
    name    : str
    height  : Optional[float] = None
    weight  : Optional[float] = None
    xp      : Optional[int] = None   
    # types   : List[PokemonTypes]
    image   : Optional[str]


class ShowPokemon(BaseModel):
    name: str
    height: Optional[float] = None
    weight: Optional[float] = None
    xp      : Optional[int] = None 
    class Config():
        orm_mode = True


class User(BaseModel):
    name    : str
    email   : str
    password: str


class GetUser():
    name    : str
    email   : str
    password: str

    class Config():
        orm_mode = True