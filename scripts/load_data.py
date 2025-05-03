import asyncio, csv, os, sys
from pathlib import Path

# Add the parent directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import insert
from app.models import FoodTruck
from dotenv import load_dotenv

load_dotenv()
DB = os.getenv("DATABASE_URL")
engine = create_async_engine(DB, echo=False)
Session = async_sessionmaker(engine, expire_on_commit=False)

CSV_PATH = "Mobile_Food_Facility_Permit.csv"

# Main function to load CSV data into the database
async def main():
    async with Session() as session:
        # Open the CSV file
        with open(CSV_PATH, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)  # Read rows as dictionaries

            # Iterate through each row in the CSV file
            for row in reader:
                # Skip rows without valid coordinates
                if not row["Latitude"] or not row["Longitude"]:
                    continue

                # Create a single FoodTruck entry dictionary
                food_truck_data = dict(
                    id=int(row["locationid"]),  # Use locationid as the primary key
                    applicant=row["Applicant"],
                    status=row["Status"],
                    address=row["Address"],
                    latitude=float(row["Latitude"]),
                    longitude=float(row["Longitude"]),
                    geom=f"SRID=4326;POINT({row['Longitude']} {row['Latitude']})",
                )

                # Insert one row at a time (no batching)
                await session.execute(insert(FoodTruck), [food_truck_data])
                await session.commit()

    await engine.dispose()
    print("Load complete!")

if __name__ == "__main__":
    asyncio.run(main())
