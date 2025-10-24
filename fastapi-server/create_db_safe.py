#!/usr/bin/env python3
"""Create DB schema safely.

This script runs SQLAlchemy's metadata.create_all() against the configured
async engine. It is defensive about asyncio event loop state (works when an
event loop is already running) and disposes the engine on completion.

Usage:
  DATABASE_URL="postgresql+asyncpg://..." python create_db_safe.py

The project layout expects the Python package to live under `src/`. If you
run this script from the repository folder it will add `src` to sys.path so
`openapi_server` imports work without needing PYTHONPATH set externally.
"""

from __future__ import annotations

import logging
import os
import sys
import threading
from pathlib import Path
from typing import Any

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("create_db")

# Ensure `src` is on sys.path so imports like `openapi_server` resolve when
# running this script from the repository folder.
HERE = Path(__file__).resolve().parent
SRC = HERE / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

try:
    # Local imports after sys.path manipulation
    from openapi_server.db import engine
    from openapi_server.db_models import metadata
except Exception as exc:  # pragma: no cover - obvious import/runtime failures
    logger.exception("Failed to import project modules: %s", exc)
    raise


async def _create_schema() -> None:
    """Run metadata.create_all using the async engine and then dispose it."""
    logger.info("Creating DB schema using DATABASE_URL=%s", os.environ.get("DATABASE_URL"))
    async with engine.begin() as conn:  # type: ignore[attr-defined]
        await conn.run_sync(metadata.create_all)
    # Dispose the engine to close pool connections and free resources.
    try:
        await engine.dispose()  # type: ignore[attr-defined]
    except Exception:
        # best-effort dispose; log but don't fail the whole run because of it
        logger.exception("Error while disposing engine")


def _run_in_new_thread(coro: Any) -> None:
    """Run `coro` in a fresh event loop inside a background thread.

    This is used when an asyncio event loop is already running in the current
    thread (common in interactive environments). Running on a dedicated
    thread avoids "attached to a different loop" errors.
    """

    def _runner() -> None:
        import asyncio

        loop = asyncio.new_event_loop()
        try:
            asyncio.set_event_loop(loop)
            loop.run_until_complete(coro)
        finally:
            try:
                loop.close()
            except Exception:
                logger.exception("Failed to close background loop")

    thread = threading.Thread(target=_runner, daemon=False)
    thread.start()
    thread.join()


def main() -> None:
    """Entry point: run the async schema creation handling running loops."""
    import asyncio

    coro = _create_schema()
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        # No running loop: safe to use asyncio.run
        asyncio.run(coro)
        return

    # If we get here, an event loop is already running in this thread.
    logger.info("Detected running event loop; delegating schema creation to a background thread")
    _run_in_new_thread(coro)


if __name__ == "__main__":
    try:
        main()
        logger.info("Schema creation complete.")
    except Exception as exc:  # pragma: no cover - bubble up errors for user visibility
        logger.exception("Schema creation failed: %s", exc)
        raise
