from sqlalchemy import Column, ForeignKey, Integer, String, Float
from database import Base
from sqlalchemy.orm import relationship


class PokemonTypeAssociation(Base):
    __tablename__ = 'pokemon_type_association'
    
    pokemon_id = Column(Integer, ForeignKey('pokemons.id'), primary_key=True)
    pokemontype_id = Column(Integer, ForeignKey('pokemontype.id'), primary_key=True)


class PokemonTeamAssociation(Base):
    __tablename__ = 'pokemon_team_association'
    team_id = Column(Integer, ForeignKey('pokemonteam.id'), primary_key=True)
    pokemon_id = Column(Integer, ForeignKey('pokemons.id'), primary_key=True)


class Pokemon(Base):
    __tablename__ = 'pokemons'

    id      = Column(Integer, primary_key = True, index = True)
    name    = Column(String)
    height  = Column(Float)
    weight  = Column(Float)
    xp      =  Column(Integer)
    image   = Column(String)

    types = relationship('PokemonAssociation')