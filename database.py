from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# sqlite db connection
# SQLALCHEMY_DATABASE_URL = "sqlite:///./data.db"
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})


# postgresql db connection--postgreql-superUser-password-localhosr-port-databaseName
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Aopeyemi98@localhost:5432/to_do_db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit = False)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




# installed for postgres connection
# pip install psycopg2-binary