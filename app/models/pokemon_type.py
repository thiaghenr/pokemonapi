from sqlalchemy import Column, Integer, String
from database import Base
from sqlalchemy.orm import relationship


class PokemonType(Base):
    __tablename__ = 'pokemontype'

    id      = Column(Integer, primary_key = True, index = True)
    name    = Column(String)
    pokemon = relationship('PokemonTypeAssociation')