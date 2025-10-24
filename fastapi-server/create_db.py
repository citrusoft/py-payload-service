import asyncio
import os
from openapi_server.db_models import metadata
from openapi_server import db


async def main() -> None:
    # engine is created from DATABASE_URL in openapi_server.db
    engine = db.engine
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)


if __name__ == "__main__":
    print("Creating DB schema using DATABASE_URL=", os.environ.get("DATABASE_URL"))
    asyncio.run(main())
    print("Schema creation complete.")
#!/bin/env python3

import asyncio
from openapi_server.db import engine
from openapi_server.db_models import metadata

async def main():
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

if __name__ == "__main__":
    print(str(metadata))
    asyncio.run(main())
    print("Schema created")
