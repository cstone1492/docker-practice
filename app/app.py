
def app_create():
    from .database.database import get_db
    global _app
    _app.sql_session = get_db()
    return _app