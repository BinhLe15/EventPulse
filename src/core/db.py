"""
Database session management and dependency injection.
Provides async SQLAlchemy engine and session factory.
"""
from fastapi.concurrency import asynccontextmanager
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from src.core.config import settings


def create_async_sessionmaker():

    try:
        engine = create_async_engine(
            str(settings.DATABASE_URL),
            pool_size=10,
            max_overflow=5,
            pool_timeout=30,
            pool_recycle=1800,
            pool_pre_ping=True,
            connect_args={
                "timeout": 30,
            },
        )
    except Exception as ex:
        print(f"Error creating async sessionmaker: {str(ex)}")
        raise
    else:
        AsyncSessionLocal = async_sessionmaker(
            bind=engine, # bind engine above to sessionmaker
            autoflush=False,
            expire_on_commit=False,
            autocommit=False,
        )

        return AsyncSessionLocal



AsyncSessionLocal = create_async_sessionmaker()


async def get_db():
    """
    Dependency helper to get a database session.
    Yields an async session and ensures proper cleanup.
    """
    db_session = AsyncSessionLocal()
    try:
        yield db_session
        await db_session.commit()
    except IntegrityError as ex:
        await db_session.rollback()
        print(f"Integrity in DB session: {str(ex)}")
        raise
    except SQLAlchemyError as ex:
        await db_session.rollback()
        print(f"SQLAlchemyError in DB session: {str(ex)}")
        raise
    except Exception as ex:
        await db_session.rollback()
        print(f"Unknown error in DB session: {str(ex)}")
        raise
    finally:
        await db_session.close()


session_context = asynccontextmanager(get_db)

