from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.configs.config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME


CONNECTION_URL = f"posgresql+psycopg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(CONNECTION_URL)

database_session = sessionmaker(engine, expire_on_commit=True)
