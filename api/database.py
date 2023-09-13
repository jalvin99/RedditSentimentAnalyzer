from databases import Database
from sqlalchemy import create_engine, MetaData

DATABASE_URL = "postgresql://postgres:llamas8243@localhost/postgres"

database = Database(DATABASE_URL)
metadata = MetaData()

engine = create_engine(DATABASE_URL)
