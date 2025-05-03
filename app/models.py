from sqlalchemy import Column, Integer, String, Float, Index
from geoalchemy2 import Geography
from app.db import Base

# Define a FoodTruck model that maps to the "food_trucks" table in the database
class FoodTruck(Base):
    __tablename__ = "food_trucks"

    # Columns in the table
    id = Column(Integer, primary_key=True)  # Using locationid from CSV as primary key
    applicant = Column(String)
    status = Column(String)
    address = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)

    # Geography column to store location as a PostGIS POINT (used for spatial queries)
    geom = Column(Geography(geometry_type="POINT", srid=4326))

    # Indexes to speed up text searches on applicant and address using trigram matching
    __table_args__ = (
        Index(
            "ix_applicant_trgm",
            "applicant",
            postgresql_using="gin", 
            postgresql_ops={"applicant": "gin_trgm_ops"}
        ),
        Index(
            "ix_address_trgm",
            "address",
            postgresql_using="gin",
            postgresql_ops={"address": "gin_trgm_ops"}
        ),
    )
