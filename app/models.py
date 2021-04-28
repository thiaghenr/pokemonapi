from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from database import Base
from typing import List
from sqlalchemy.orm import relationship


class Pokemon(Base):
    __tablename__ = 'pokemons'

    id      = Column(Integer, primary_key = True, index = True)
    name    = Column(String)
    height  = Column(Float)
    weight  = Column(Float)
    xp      =  Column(Integer)
    image   = Column(String)

    # types = relationship('PokemonType', back_populates = 'pokemon')

class PokemonType(Base):
    __tablename__ = 'pokemontype'

    id      = Column(Integer, primary_key = True, index = True)
    name    = Column(String)
    # pokemon = relationship('Pokemon', back_populates = 'types')


class User(Base):
    __tablename__ = 'users'

    id      = Column(Integer, primary_key = True, index = True)
    name    = Column(String)
    email   = Column(String)
    password= Column(String)
