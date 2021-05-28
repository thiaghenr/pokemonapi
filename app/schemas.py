from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import relationship

#{"id": 1, "name": "bulbasaur", "height": 0.7, "weight": 6.9, "xp": 64, "types": ["poison", "grass"], "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png"}


class PokemonType(BaseModel):
    name: str

    # class Config:
    #     arbitrary_types_allowed = True



class Pokemon(BaseModel):
    name    : str
    height  : Optional[float] = None
    weight  : Optional[float] = None
    xp      : Optional[int] = None   
    types   : List[PokemonType] = []
    image   : Optional[str]

    # class Config:
    #     arbitrary_types_allowed = True



class User(BaseModel):
    name    : str
    email   : str
    password: str


class GetUser(BaseModel):
    name    : str
    email   : str

    class Config():
        orm_mode = True


class ShowPokemonType(BaseModel):
    name: str

    class Config():
        orm_mode = True
        # arbitrary_types_allowed = True


class ShowPokemon(BaseModel):
    name: str
    height: Optional[float] = None
    weight: Optional[float] = None
    xp      : Optional[int] = None 
    types : List[ShowPokemonType] = None
    
    class Config():
        orm_mode = True
        # arbitrary_types_allowed = True