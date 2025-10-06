from sqlalchemy import Text, create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "mysql+pymysql://root:1111@localhost/ecommerce"

engine = create_engine(DATABASE_URL, echo=True)

Base = declarative_base()

class Seller(Base):
    __tablename__ = "Seller"
    id = Column(Integer, primary_key=True, autoincrement=True)
    storename = Column(String(50), nullable=False)
    ownername = Column(String(50), nullable=False)
    email = Column(String(120), nullable=False, unique=True)
    phone = Column(String(20), nullable=False)
    gst = Column(String(30), nullable=False, unique=True)
    desc = Column(Text)
Base.metadata.create_all(engine)

# print("✅ Tables created successfully!")


SessionLocal = sessionmaker(bind=engine)