from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create SQLAlchemy engine
# SQLALCHEMY_DATABASE_URL = "mysql://user:pass@hostname/database"
SQLALCHEMY_DATABASE_URL = "mysql://root:1234@localhost/lesoiree"

# Create connection to database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
