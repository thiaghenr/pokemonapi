from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'sqlite:///./test.db'

test_engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args = {"check_same_thread": False})

TestingSessionLocal = sessionmaker(bind = test_engine, autocommit = False, autoflush = False)

Test_Base = declarative_base()

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()