import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient


def _make_sqlite_url(path: Path) -> str:
    return f"sqlite+aiosqlite:///{path}"


async def _create_db_and_insert(engine, metadata, PayloadORM):
    # create tables and insert two rows
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy.orm import sessionmaker

    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        a = PayloadORM(origin="MLB", destination="CLT", julian_do_y=22, passengers=200, baggage=20000.0, cargo=500.0)
        b = PayloadORM(origin="MLB", destination="MIA", julian_do_y=11, passengers=100, baggage=10000.0, cargo=100.0)
        session.add_all([a, b])
        await session.commit()


@pytest.fixture()
def client(tmp_path, monkeypatch):
    # create a temp sqlite file for this test
    db_file = tmp_path / "test_payloads.db"
    database_url = _make_sqlite_url(db_file)

    # create engine and replace in openapi_server.db
    from sqlalchemy.ext.asyncio import create_async_engine

    engine = create_async_engine(database_url, echo=False, future=True)

    import openapi_server.db as dbmod
    import openapi_server.db_models as dbmodels

    # monkeypatch the engine and async_session factory
    monkeypatch.setattr(dbmod, "engine", engine)
    # rebuild async_session
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.ext.asyncio import AsyncSession

    dbmod.async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    # populate DB using asyncio.run to ensure an event loop exists
    import asyncio as _asyncio
    _asyncio.run(_create_db_and_insert(engine, dbmodels.metadata, dbmodels.PayloadORM))

    # ensure the db module is reloaded so startup uses patched engine
    import importlib
    importlib.reload(dbmod)

    from openapi_server.main import app

    with TestClient(app) as c:
        yield c


def test_get_all_payloads_happy(client):
    resp = client.get('/payloads', params={'offset': 0, 'limit': 3})
    assert resp.status_code == 200
    data = resp.json()
    assert data['total'] == 2
    assert len(data['data']) == 2


def test_get_all_payloads_invalid_param(client):
    resp = client.get('/payloads', params={'offset': 'notint', 'limit': 3})
    assert resp.status_code == 422
