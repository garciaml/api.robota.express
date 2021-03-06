from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# user = os.environ["DB_USER"]
# password = os.environ["DB_PASS"]
# host = os.environ["DB_HOST"]
# port = os.environ["DB_PORT"]
# database = os.environ["DB_NAME"]

# SQLALCHEMY_DATABASE_URL = f"mysql://{user}:{password}@{host}:{port}/{database}"
# SQLALCHEMY_DATABASE_URL = "mysql+mysqldb://dev:dev@127.0.0.1:3306/fitness"
SQLALCHEMY_DATABASE_URL = "sqlite:///dev-sqlite-database.db"

# If SQLite database, put connect_args={"check_same_thread": False}
# engine = create_engine(SQLALCHEMY_DATABASE_URL)
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
