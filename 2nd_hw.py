import uvicorn
from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

DB_URL = "sqlite+aiosqlite:///pet_shop.db"
engine = create_async_engine(DB_URL)

class Base(DeclarativeBase):
    pass

class ClientModel(Base):
    __tablename__ = "clients"

    identifier: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str]
    username: Mapped[str] = mapped_column(unique=True)
    secret: Mapped[str]

class PetModel(Base):
    __tablename__ = "pets"

    identifier: Mapped[int] = mapped_column(primary_key=True)
    category: Mapped[str]
    title: Mapped[str]
    years: Mapped[int]

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

class SignupRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=40)
    username: str = Field(min_length=4, max_length=20, pattern=r"^[a-z0-9_]+$")
    secret: str = Field(min_length=6, max_length=64)

class ClientResponse(BaseModel):
    identifier: int
    full_name: str
    username: str

@app.post("/register")
def register(payload: SignupRequest) -> ClientResponse:
    new_client = ClientResponse(
        identifier=1,
        full_name=payload.full_name,
        username=payload.username,
    )
    return new_client

if __name__ == "__main__":
    uvicorn.run(app)
