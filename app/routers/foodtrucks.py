from typing import List, Optional

from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.models import FoodTruck
from app.schemas import FoodTruckOut

# Create a router for all truck-related endpoints
router = APIRouter(
    prefix="/trucks",     # All routes will be prefixed with /trucks
    tags=["trucks"]       # Group name for the Swagger UI
)

# Default status used for filtering
DEFAULT_STATUS = "APPROVED"

# Add OPTIONS handler for all routes
@router.options("/{path:path}")
async def options_handler(path: str, response: Response):
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:5173"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return {}

# Search food trucks by applicant name
@router.get("/by-applicant", response_model=List[FoodTruckOut])
async def by_applicant(
    q: str = Query(..., description="Search term for Applicant name"),
    status: Optional[str] = Query(None, description="Filter by permit status"),
    db: AsyncSession = Depends(get_db),
):
    """
    Search food trucks by a partial match on the applicant name.
    Optionally filter by status (default: 'APPROVED').
    """
    async with db as session:
        stmt = select(FoodTruck).where(FoodTruck.applicant.ilike(f"%{q}%"))
        if status and status.strip():
            stmt = stmt.where(FoodTruck.status == status)
        result = await session.scalars(stmt)
        return result.all()

# Search food trucks by street address
@router.get("/by-street", response_model=List[FoodTruckOut])
async def by_street(
    street: str = Query(..., description="Partial street name, e.g., 'Market'"),
    status: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    """
    Search food trucks by a partial match on street address.
    Optionally filter by status.
    """
    async with db as session:
        stmt = select(FoodTruck).where(FoodTruck.address.ilike(f"%{street}%"))
        if status and status.strip():
            stmt = stmt.where(FoodTruck.status == status)
        result = await session.scalars(stmt)
        return result.all()

# Find nearby food trucks using geolocation
@router.get("/nearby", response_model=List[FoodTruckOut])
async def nearby(
    lat: float = Query(..., ge=-90, le=90, description="Latitude (-90 to 90)"),
    lng: float = Query(..., ge=-180, le=180, description="Longitude (-180 to 180)"),
    n: int = Query(5, gt=0, le=20, description="Number of trucks to return (max 20)"),
    status: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    """
    Find the closest food trucks to a given latitude/longitude.
    Returns up to 'n' results (default 5), ordered by distance.
    """
    async with db as session:
        # Create a point from the given lat/lng
        point = func.ST_SetSRID(func.ST_MakePoint(lng, lat), 4326)

        # Compute distance between each truck's location and the given point
        distance = func.ST_Distance(FoodTruck.geom, point)

        # Build query to order trucks by distance and limit the number returned
        stmt = select(FoodTruck).order_by(distance).limit(n)
        if status and status.strip():
            stmt = stmt.where(FoodTruck.status == status)

        result = await session.scalars(stmt)
        return result.all()