from pydantic import BaseModel
from typing import List
from user import User


class PokemonTeam(BaseModel):
    name    : str
    coach   : User
    pokemons: List[Pokemon]


class ShowPokemonTeam(BaseModel):
    name    : str
    coach   : User
    pokemons: List[Pokemon]

    class Config():
        orm_mode = True