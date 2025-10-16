from typing import Dict, List, Optional

from fastapi import HTTPException, Response

from openapi_server.apis.payloads_api_base import BasePayloadsApi
from openapi_server.models.payload import Payload
from openapi_server.models.get_all_payloads200_response import GetAllPayloads200Response


class PayloadsApiImpl(BasePayloadsApi):
    """Simple in-memory implementation for the Payloads API.

    This keeps data in a module-level dict for simplicity. It's suitable for
    development and tests. The OpenAPI-generated server will import this
    module automatically because it lives under `impl` and subclasses the
    generated base class.
    """

    _store: Dict[int, Payload] = {}
    _next_id: int = 1

    async def create_payload(self, payload: Optional[Payload]) -> Payload:
        if payload is None:
            raise HTTPException(status_code=400, detail="Missing payload")

        # assign id if not provided
        if payload.id is None:
            payload.id = self._next_id
            PayloadsApiImpl._next_id += 1
        else:
            # ensure next id is beyond any provided id
            if payload.id >= PayloadsApiImpl._next_id:
                PayloadsApiImpl._next_id = payload.id + 1

        # save a copy in store
        PayloadsApiImpl._store[int(payload.id)] = payload

        return payload

    async def get_all_payloads(self, offset: Optional[int], limit: Optional[int]) -> GetAllPayloads200Response:
        off = int(offset or 0)
        lim = int(limit or 5)
        items: List[Payload] = list(PayloadsApiImpl._store.values())
        total = len(items)
        paged = items[off: off + lim]

        return GetAllPayloads200Response(offset=off, limit=lim, total=total, data=paged)

    async def get_payload(self, id: int) -> Payload:
        payload = PayloadsApiImpl._store.get(int(id))
        if not payload:
            raise HTTPException(status_code=404, detail="Payload not found")
        return payload

    async def update_payload(self, id: int, payload: Optional[Payload]) -> Payload:
        if payload is None:
            raise HTTPException(status_code=400, detail="Missing payload")

        if int(id) not in PayloadsApiImpl._store:
            raise HTTPException(status_code=404, detail="Payload not found")

        # keep id consistent with path
        payload.id = int(id)
        PayloadsApiImpl._store[int(id)] = payload
        return payload

    async def delete_payload(self, id: int) -> Response:
        if int(id) not in PayloadsApiImpl._store:
            raise HTTPException(status_code=404, detail="Payload not found")
        del PayloadsApiImpl._store[int(id)]
        return Response(status_code=204)
