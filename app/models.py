from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Table
from database import Base
from typing import List
from sqlalchemy.orm import relationship



class PokemonAssociation(Base):
    __tablename__ = 'pokemon_association_table'
    
    pokemon_id = Column(Integer, ForeignKey('pokemons.id'), primary_key=True)
    pokemontype_id = Column(Integer, ForeignKey('pokemontype.id'), primary_key=True)



class Pokemon(Base):
    __tablename__ = 'pokemons'

    id      = Column(Integer, primary_key = True, index = True)
    name    = Column(String)
    height  = Column(Float)
    weight  = Column(Float)
    xp      =  Column(Integer)
    image   = Column(String)

    types = relationship('PokemonAssociation')

class PokemonType(Base):
    __tablename__ = 'pokemontype'

    id      = Column(Integer, primary_key = True, index = True)
    name    = Column(String)
    pokemon = relationship('PokemonAssociation')

class User(Base):
    __tablename__ = 'users'

    id      = Column(Integer, primary_key = True, index = True)
    name    = Column(String)
    email   = Column(String)
    password= Column(String)
