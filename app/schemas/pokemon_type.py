from pydantic import BaseModel

class PokemonType(BaseModel):
    name: str


class ShowPokemonType(BaseModel):
    name: str
    class Config():
        orm_mode = True