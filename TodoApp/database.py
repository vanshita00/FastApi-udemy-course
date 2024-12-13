# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base

# SQLALCHEMY_DATABASE_URL='mysql+pymysql://root:vanshita1234%40@127.0.0.1:3306/TodoApplicationDatabase'


# engine=create_engine(SQLALCHEMY_DATABASE_URL,connect_args={'check_same_thread':False})

# SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

# Base=declarative_base()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Correct connection string
SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:vanshita1234%40@127.0.0.1:3306/TodoApplicationDatabase'

# Create the engine without `connect_args`
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create session and Base
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

