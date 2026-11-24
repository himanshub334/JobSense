from sqlalchemy import create_engine,event
from sqlalchemy.orm import DeclarativeBase,sessionmaker
from pgvector.psycopg import register_vector
from .config import settings
engine=create_engine(settings.database_url,pool_pre_ping=True)
@event.listens_for(engine,"connect")
def vector_type(conn,record):
    try: register_vector(conn)
    except Exception: pass
class Base(DeclarativeBase): pass
Session=sessionmaker(bind=engine,autoflush=False,expire_on_commit=False)
def get_db():
    db=Session()
    try: yield db
    finally: db.close()
