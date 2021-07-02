from sqlalchemy import Column, ForeignKey, Integer, String
from database import Base

class UserTeamAssociation(Base):
    __tablename__ = 'user_team_association'

    team_id = Column(Integer, ForeignKey('pokemonteam.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)


class User(Base):
    __tablename__ = 'users'

    id      = Column(Integer, primary_key = True, index = True)
    name    = Column(String)
    email   = Column(String)
    password= Column(String)