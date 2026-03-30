import pytest_asyncio
from sqlalchemy.pool import StaticPool
from src.api.core.database import Base, get_db
from src.api.main import app
from src.api.models.models import Data
from httpx import ASGITransport, AsyncClient
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

# -----------------------------
# Configuração do banco de teste
# -----------------------------
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    poolclass=StaticPool
)
TestingSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


# -----------------------------
# Override da dependência FastAPI
# -----------------------------
async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


# -----------------------------
# Fixture para criar schema DB
# -----------------------------
@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_db():
    """
    Cria as tabelas do banco de dados em memória antes de qualquer teste.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # opcional: limpar após todos os testes
    await engine.dispose()


# -----------------------------
# Fixture HTTP client async
# -----------------------------
@pytest_asyncio.fixture
async def client(db):
    async def override():
        yield db

    app.dependency_overrides[get_db] = override

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac


# -----------------------------
# Fixture do DB async para testes diretos
# -----------------------------
@pytest_asyncio.fixture
async def db():
    async with TestingSessionLocal() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture
async def clean_db(db):
    await db.execute(delete(Data))
    await db.commit()
    yield db
