import pytest
import logging

logger = logging.getLogger(__name__)

# Test the ping endpoint
@pytest.mark.asyncio
async def test_ping(client):
    logger.info("Testing ping endpoint...")
    r = await client.get("/ping")
    if r.status_code == 200 and r.json() == {"message": "pong!"}:
        logger.info("✅ Ping test passed successfully")
    else:
        logger.error(f"Expected status 200, got {r.status_code}")
        logger.error(f"Expected response {{'message': 'pong!'}}, got {r.json()}")
        logger.error("❌ Ping test failed")
    assert r.status_code == 200 and r.json() == {"message": "pong!"}

# Test the by-applicant endpoint
@pytest.mark.asyncio
async def test_by_applicant(client):
    logger.info("Testing search by applicant endpoint with query 'MOMO'...")
    r = await client.get("/trucks/by-applicant", params={"q": "MOMO"})
    data = r.json()
    
    logger.info(f"Response status: {r.status_code}")
    
    # Check for MOMO INNOVATION LLC
    applicants = [truck["applicant"] for truck in data]
    momo_count = len([truck for truck in data if truck["applicant"] == "MOMO INNOVATION LLC"])
    
    if "MOMO INNOVATION LLC" in applicants and momo_count >= 1:
        logger.info(f"Found {momo_count} entries for MOMO INNOVATION LLC")
        logger.info("✅ Applicant search test passed successfully")
    else:
        logger.error(f"Expected to find MOMO INNOVATION LLC, found: {applicants}")
        logger.error("❌ Applicant search test failed")
    
    assert "MOMO INNOVATION LLC" in applicants
    assert momo_count >= 1

# Test the by-street endpoint with a status filter
@pytest.mark.asyncio
async def test_by_street_status_filter(client):
    logger.info("Testing search by street endpoint with street 'SAN' and status 'APPROVED'...")
    r = await client.get("/trucks/by-street", params={"street": "SAN", "status": "APPROVED"})
    data = r.json()
    
    logger.info(f"Response status: {r.status_code}")
    
    expected = [
        {
            "id": 1591820,
            "applicant": "Truly Food & More",
            "status": "APPROVED",
            "address": "217 SANSOME ST",
            "latitude": 37.79238986198323,
            "longitude": -122.40126969523558
        },
        {
            "id": 1585966,
            "applicant": "Curry Up Now",
            "status": "APPROVED",
            "address": "727 SANSOME ST",
            "latitude": 37.79694900602121,
            "longitude": -122.40218343189426
        }
    ]
    
    missing_trucks = []
    for truck in expected:
        if not any(all(truck[k] == d.get(k) for k in truck) for d in data):
            missing_trucks.append(truck["id"])
    
    if not missing_trucks:
        logger.info(f"Found all expected trucks: {[t['id'] for t in expected]}")
        logger.info("✅ Street search test passed successfully")
    else:
        logger.error(f"Missing trucks with IDs: {missing_trucks}")
        logger.error("❌ Street search test failed")
    
    for truck in expected:
        assert any(all(truck[k] == d.get(k) for k in truck) for d in data), f"Truck {truck['id']} not found in response"

# Test the nearby endpoint
@pytest.mark.asyncio
async def test_nearby(client):
    logger.info("Testing nearby endpoint with lat=37.792, lng=-122.398, status=APPROVED...")
    r = await client.get("/trucks/nearby", params={"lat": 37.792, "lng": -122.398, "status": "APPROVED"})
    data = r.json()
    
    logger.info(f"Response status: {r.status_code}")
    
    expected = [
        {
            "id": 1568883,
            "applicant": "Senor Sisig",
            "status": "APPROVED",
            "address": "101 CALIFORNIA ST",
            "latitude": 37.792948952834664,
            "longitude": -122.39809861316652
        },
        {
            "id": 1565571,
            "applicant": "MOMO INNOVATION LLC",
            "status": "APPROVED",
            "address": "101 CALIFORNIA ST",
            "latitude": 37.792948952834664,
            "longitude": -122.39809861316652
        },
        {
            "id": 1568997,
            "applicant": "Think is Good Inc.",
            "status": "APPROVED",
            "address": "100 PINE ST",
            "latitude": 37.79264071673365,
            "longitude": -122.39897033211076
        },
        {
            "id": 1577112,
            "applicant": "BOWL'D ACAI, LLC.",
            "status": "APPROVED",
            "address": "111 BATTERY ST",
            "latitude": 37.79236678688307,
            "longitude": -122.40014830676716
        },
        {
            "id": 1565413,
            "applicant": "MOMO INNOVATION LLC",
            "status": "APPROVED",
            "address": "1 BUSH ST",
            "latitude": 37.79092150726921,
            "longitude": -122.4001004237385
        }
    ]
    
    missing_trucks = []
    for truck in expected:
        if not any(all(truck[k] == d.get(k) for k in truck) for d in data):
            missing_trucks.append(truck["id"])
    
    if not missing_trucks:
        logger.info(f"Found all expected trucks: {[t['id'] for t in expected]}")
        logger.info("✅ Nearby search test passed successfully")
    else:
        logger.error(f"Missing trucks with IDs: {missing_trucks}")
        logger.error("❌ Nearby search test failed")
    
    for truck in expected:
        assert any(all(truck[k] == d.get(k) for k in truck) for d in data), f"Truck {truck['id']} not found in response"
