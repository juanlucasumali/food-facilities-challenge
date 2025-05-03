from fastapi import FastAPI

app = FastAPI(title="SF Food Trucks API", version="0.0.1")


@app.get("/ping")
async def ping() -> dict[str, str]:
    """Liveness probe."""
    return {"message": "pong!"}
