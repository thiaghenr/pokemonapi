from sqlalchemy import Column, Integer, String
from database import Base
from sqlalchemy.orm import relationship

class PokemonTeam(Base):
    __tablename__ = 'pokemonteam'

    id = Column(Integer, primary_key = True, index = True)
    name = Column(String)
    pokemons = relationship('PokemonTeamAssociation')
    coach = relationship('UserTeamAssociation')