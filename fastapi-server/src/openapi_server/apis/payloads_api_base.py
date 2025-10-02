# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from pydantic import Field, StrictInt
from typing import Optional
from typing_extensions import Annotated
from openapi_server.models.error import Error
from openapi_server.models.get_all_payloads200_response import GetAllPayloads200Response
from openapi_server.models.payload import Payload


class BasePayloadsApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BasePayloadsApi.subclasses = BasePayloadsApi.subclasses + (cls,)
    async def create_payload(
        self,
        payload: Annotated[Optional[Payload], Field(description="Payload Details")],
    ) -> Payload:
        """Use this endpoint to add a new route to the estimator"""
        ...


    async def delete_payload(
        self,
        id: StrictInt,
    ) -> Payload:
        """Use this endpoint to remove a payload from the estimator."""
        ...


    async def get_all_payloads(
        self,
        offset: Optional[StrictInt],
        limit: Optional[StrictInt],
    ) -> GetAllPayloads200Response:
        """Use this endpoint to browse all payloads in the estimator."""
        ...


    async def get_payload(
        self,
        id: StrictInt,
    ) -> Payload:
        """Use this endpoint to get the estimate for a specific route."""
        ...


    async def update_payload(
        self,
        id: StrictInt,
        payload: Annotated[Optional[Payload], Field(description="Payload Details")],
    ) -> Payload:
        """Use this endpoint to update the payload with actuals."""
        ...
