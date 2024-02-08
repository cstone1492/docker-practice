from fastapi import FastAPI
def app_create():
    from .database.database import session_init
    from .database.schema import engine_init
    global _app
    _app = FastAPI()
    _app.sql_engine= engine_init()
    _app.sql_session = session_init(_app.sql_engine)
    return _app