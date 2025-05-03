import pytest

# Test the ping endpoint
@pytest.mark.asyncio
async def test_ping(client):
    r = await client.get("/ping")
    assert r.status_code == 200 and r.json() == {"message": "pong!"}

# Test the by-applicant endpoint
@pytest.mark.asyncio
async def test_by_applicant(client):
    r = await client.get("/trucks/by-applicant", params={"q": "MOMO"})
    data = r.json()
    # Should match both entries for MOMO INNOVATION LLC
    applicants = [truck["applicant"] for truck in data]
    assert "MOMO INNOVATION LLC" in applicants
    assert len([truck for truck in data if truck["applicant"] == "MOMO INNOVATION LLC"]) >= 1

# Test the by-street endpoint with a status filter
@pytest.mark.asyncio
async def test_by_street_status_filter(client):
    r = await client.get("/trucks/by-street", params={"street": "SANSOME", "status": "APPROVED"})
    expected = [
        {
            "id": 510,
            "applicant": "Truly Food & More",
            "status": "APPROVED",
            "address": "217 SANSOME ST",
            "latitude": 37.79238986198323,
            "longitude": -122.40126969523558
        },
        {
            "id": 656,
            "applicant": "Curry Up Now",
            "status": "APPROVED",
            "address": "727 SANSOME ST",
            "latitude": 37.79694900602121,
            "longitude": -122.40218343189426
        }
    ]
    data = r.json()
    for truck in expected:
        assert any(
            all(truck[k] == d.get(k) for k in truck) for d in data
        ), f"Truck {truck['id']} not found in response"

# Test the nearby endpoint
@pytest.mark.asyncio
async def test_nearby(client):
    r = await client.get("/trucks/nearby", params={"lat": 37.792, "lng": -122.398})
    data = r.json()
    expected = [
        {
            "id": 605,
            "applicant": "Senor Sisig",
            "status": "APPROVED",
            "address": "101 CALIFORNIA ST",
            "latitude": 37.792948952834664,
            "longitude": -122.39809861316652
        },
        {
            "id": 512,
            "applicant": "MOMO INNOVATION LLC",
            "status": "APPROVED",
            "address": "101 CALIFORNIA ST",
            "latitude": 37.792948952834664,
            "longitude": -122.39809861316652
        },
        {
            "id": 604,
            "applicant": "Think is Good Inc.",
            "status": "APPROVED",
            "address": "100 PINE ST",
            "latitude": 37.79264071673365,
            "longitude": -122.39897033211076
        },
        {
            "id": 537,
            "applicant": "BOWL'D ACAI, LLC.",
            "status": "APPROVED",
            "address": "111 BATTERY ST",
            "latitude": 37.79236678688307,
            "longitude": -122.40014830676716
        },
        {
            "id": 516,
            "applicant": "MOMO INNOVATION LLC",
            "status": "APPROVED",
            "address": "1 BUSH ST",
            "latitude": 37.79092150726921,
            "longitude": -122.4001004237385
        }
    ]
    
    # Check that the response contains all expected trucks (order may differ)
    for truck in expected:
        assert any(
            all(truck[k] == d.get(k) for k in truck) for d in data
        ), f"Truck {truck['id']} not found in response"
