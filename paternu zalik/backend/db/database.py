"""Database connection singleton module."""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from backend.config import MYSQL_URL, MYSQL_DATABASE, MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT
from typing import Optional, AsyncGenerator
import aiomysql


class DatabaseConnection:
    """Singleton class for managing database connections."""
    
    _instance: Optional['DatabaseConnection'] = None
    
    def __init__(self) -> None:
        if DatabaseConnection._instance is not None:
            raise RuntimeError("Use get_instance() instead")
        self._engine = None
        self._session_maker = None
        self._base = None
        self._initialize()

    @classmethod
    def get_instance(cls) -> 'DatabaseConnection':
        if cls._instance is None:
            cls._instance = DatabaseConnection()
        return cls._instance

    async def create_database(self) -> None:
        """Create database if it doesn't exist."""
        conn = None
        try:
            conn = await aiomysql.connect(
                host=MYSQL_HOST,
                port=MYSQL_PORT,
                user=MYSQL_USER,
                password=MYSQL_PASSWORD
            )
            async with conn.cursor() as cur:
                await cur.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DATABASE}")
                await conn.commit()
        except Exception as e:
            print(f"Error creating database: {e}")
            raise e
        finally:
            if conn:
                conn.close()  # Note: using sync close() instead of await

    def _initialize(self) -> None:
        """Initialize database engine and session maker."""
        if not self._engine:
            self._engine = create_async_engine(
                MYSQL_URL,
                echo=True,
                pool_pre_ping=True
            )
            self._session_maker = sessionmaker(
                self._engine,
                class_=AsyncSession,
                expire_on_commit=False
            )
            self._base = declarative_base()

    @property
    def engine(self):
        return self._engine

    @property
    def session_maker(self):
        return self._session_maker

    @property
    def base(self):
        return self._base

    async def close(self) -> None:
        if self._engine:
            await self._engine.dispose()
            self._engine = None
            self._session_maker = None


# Create single instance
db = DatabaseConnection.get_instance()
Base = db.base


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with db.session_maker() as session:
        yield session
