from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'postgresql://username:password@postgresql:5432/database?sslmode=disable'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def session_init(db_engine):
    from sqlalchemy.orm import sessionmaker
    session_factory = sessionmaker(bind=db_engine)
    return session_factory