from pydantic import BaseModel
from typing import List, Optional
from .pokemon_type import PokemonType, ShowPokemonType


class Pokemon(BaseModel):
    name    : str
    height  : Optional[float] = None
    weight  : Optional[float] = None
    xp      : Optional[int] = None   
    types   : List[PokemonType] = []
    image   : Optional[str]


class ShowPokemon(BaseModel):
    name: str
    height: Optional[float] = None
    weight: Optional[float] = None
    xp      : Optional[int] = None 
    types : List[ShowPokemonType] = None
    
    
    class Config():
        orm_mode = True

