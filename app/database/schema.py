from content.database.database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text
from sqlalchemy import JSON, CheckConstraint, Column, ForeignKey, Integer
from sqlalchemy import \
    Uuid as \
    UUIDType  # native  (this is old news - https://stackoverflow.com/q/183042)
from sqlalchemy import delete, select, types
from sqlalchemy.ext.mutable import Mutable, MutableList
from sqlalchemy.orm import (DeclarativeBase, Mapped, Session, backref,
                            declarative_base, mapped_column, relationship)
import datetime as dt
import uuid
from typing import Annotated, Dict, List, NamedTuple, Tuple, Union

class Base(DeclarativeBase):
    pass

# DeclarativeBase = declarative_base()
def create_unique_id():
    return uuid.uuid4()


def create_updatetime():
    return dt.datetime.utcnow()

class Post(Base):
    __tablename__ = "posts"

    id = Column(UUIDType,primary_key=True,nullable=False)
    title = Column(String,nullable=False)
    content = Column(String,nullable=False)
    published = Column(Boolean, server_default='TRUE')
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    def create_unique_id(self):
        self.id = create_unique_id()

def engine_init(config):
    from sqlalchemy import create_engine
    db_config = config['database']
    if db_config['type'] == 'postgres':
        url = f"postgresql://{db_config['user']}:{db_config['password']}@postgres:{db_config['port']}/{db_config['db']}?sslmode={db_config['sslmode']}"
    else:
        return 'unknown db type'
    # sql_engine = create_engine('postgresql://username:password@postgres:5432/database?sslmode=disable')
    sql_engine = create_engine(url)
    Base.metadata.create_all(bind=sql_engine)
    return sql_engine