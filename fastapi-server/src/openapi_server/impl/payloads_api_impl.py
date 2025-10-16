from typing import Optional

from fastapi import HTTPException, Response
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from openapi_server.apis.payloads_api_base import BasePayloadsApi
from openapi_server.models.payload import Payload
from openapi_server.models.get_all_payloads200_response import GetAllPayloads200Response
from openapi_server.db import get_session
from openapi_server.db_models import PayloadORM


class PayloadsApiImpl(BasePayloadsApi):
    async def create_payload(self, payload: Optional[Payload]) -> Payload:
        if payload is None:
            raise HTTPException(status_code=400, detail="Missing payload")

        async for session in get_session():
            orm = PayloadORM(
                origin=payload.origin,
                destination=payload.destination,
                julian_do_y=payload.julian_do_y,
                passengers=payload.passengers,
                baggage=payload.baggage,
                cargo=payload.cargo,
            )
            session.add(orm)
            await session.commit()
            await session.refresh(orm)

            return Payload.from_dict({
                "id": orm.id,
                "origin": orm.origin,
                "destination": orm.destination,
                "julianDoY": orm.julian_do_y,
                "passengers": orm.passengers,
                "baggage": orm.baggage,
                "cargo": orm.cargo,
            })

    async def get_all_payloads(self, offset: Optional[int], limit: Optional[int]) -> GetAllPayloads200Response:
        off = int(offset or 0)
        lim = int(limit or 5)
        async for session in get_session():
            result = await session.execute(select(PayloadORM).offset(off).limit(lim))
            items = result.scalars().all()
            total_res = await session.execute(select(PayloadORM))
            total = len(total_res.scalars().all())

            data = []
            for orm in items:
                data.append(
                    Payload.from_dict({
                        "id": orm.id,
                        "origin": orm.origin,
                        "destination": orm.destination,
                        "julianDoY": orm.julian_do_y,
                        "passengers": orm.passengers,
                        "baggage": orm.baggage,
                        "cargo": orm.cargo,
                    })
                )

            return GetAllPayloads200Response(offset=off, limit=lim, total=total, data=data)

    async def get_payload(self, id: int) -> Payload:
        async for session in get_session():
            result = await session.get(PayloadORM, int(id))
            if not result:
                raise HTTPException(status_code=404, detail="Payload not found")
            orm = result
            return Payload.from_dict({
                "id": orm.id,
                "origin": orm.origin,
                "destination": orm.destination,
                "julianDoY": orm.julian_do_y,
                "passengers": orm.passengers,
                "baggage": orm.baggage,
                "cargo": orm.cargo,
            })

    async def update_payload(self, id: int, payload: Optional[Payload]) -> Payload:
        if payload is None:
            raise HTTPException(status_code=400, detail="Missing payload")
        async for session in get_session():
            orm = await session.get(PayloadORM, int(id))
            if not orm:
                raise HTTPException(status_code=404, detail="Payload not found")

            orm.origin = payload.origin
            orm.destination = payload.destination
            orm.julian_do_y = payload.julian_do_y
            orm.passengers = payload.passengers
            orm.baggage = payload.baggage
            orm.cargo = payload.cargo

            session.add(orm)
            await session.commit()
            await session.refresh(orm)

            return Payload.from_dict({
                "id": orm.id,
                "origin": orm.origin,
                "destination": orm.destination,
                "julianDoY": orm.julian_do_y,
                "passengers": orm.passengers,
                "baggage": orm.baggage,
                "cargo": orm.cargo,
            })

    async def delete_payload(self, id: int) -> Response:
        async for session in get_session():
            orm = await session.get(PayloadORM, int(id))
            if not orm:
                raise HTTPException(status_code=404, detail="Payload not found")
            await session.delete(orm)
            await session.commit()
            return Response(status_code=204)
