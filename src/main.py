from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database.session import get_db
# Note: get_db is in infrastructure, so main.py might not need changes if it uses get_db directly.
# Let's check if main.py uses dependencies from api/dependencies.py. It does not.
# However, verify_di DOES.
from sqlalchemy import text

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    """
    Simple health check ensuring DB connection works via DI.
    """
    try:
        # Simple query to check connection
        await db.execute(text("SELECT 1"))
        return {"status": "ok", "db": "connected"}
    except Exception as e:
        return {"status": "error", "db": str(e)}