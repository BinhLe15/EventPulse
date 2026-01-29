from src.core.db import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
import uvicorn
from pathlib import Path

from src.core.registrar import register_app
import src.models  # Register models
from src.core.config import settings

app = register_app()

if __name__ == "__main__":
    try:
        uvicorn.run(
            app=f"{Path(__file__).stem}:app",
            host=settings.UVICORN_HOST,
            port=settings.UVICORN_PORT,
            reload=settings.UVICORN_RELOAD,
            access_log=False,
            forwarded_allow_ips="*",
            proxy_headers=True,
        )
    except Exception as e:
        print(f"Fast API start failed: {e}")

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