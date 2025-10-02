# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.payloads_api_base import BasePayloadsApi
import openapi_server.impl

from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    HTTPException,
    Path,
    Query,
    Response,
    Security,
    status,
)

from openapi_server.models.extra_models import TokenModel  # noqa: F401
from pydantic import Field, StrictInt
from typing import Optional
from typing_extensions import Annotated
from openapi_server.models.error import Error
from openapi_server.models.get_all_payloads200_response import GetAllPayloads200Response
from openapi_server.models.payload import Payload


router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.post(
    "/payloads",
    responses={
        200: {"model": Payload, "description": "Payload Details"},
        401: {"model": Error, "description": "UnauthorizedResponse. Authentication required"},
        403: {"model": Error, "description": "You do not have enough rights to perform this operation"},
        4XX: {"model": Error, "description": "Client error"},
        "default": {"model": Error, "description": "Unexpected error"},
    },
    tags=["Payloads"],
    summary="Create a new payload",
    response_model_by_alias=True,
)
async def create_payload(
    payload: Annotated[Optional[Payload], Field(description="Payload Details")] = Body(None, description="Payload Details"),
) -> Payload:
    """Use this endpoint to add a new route to the estimator"""
    if not BasePayloadsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BasePayloadsApi.subclasses[0]().create_payload(payload)


@router.delete(
    "/payloads/{id}",
    responses={
        204: {"model": Payload, "description": "Payload Details"},
        401: {"model": Error, "description": "UnauthorizedResponse. Authentication required"},
        403: {"model": Error, "description": "You do not have enough rights to perform this operation"},
        404: {"model": Error, "description": "Resource not found"},
        4XX: {"model": Error, "description": "Client error"},
        "default": {"model": Error, "description": "Unexpected error"},
    },
    tags=["Payloads"],
    summary="Delete payload",
    response_model_by_alias=True,
)
async def delete_payload(
    id: StrictInt = Path(..., description=""),
) -> Payload:
    """Use this endpoint to remove a payload from the estimator."""
    if not BasePayloadsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BasePayloadsApi.subclasses[0]().delete_payload(id)


@router.get(
    "/payloads",
    responses={
        200: {"model": GetAllPayloads200Response, "description": "Paginated array of payloads"},
        401: {"model": Error, "description": "UnauthorizedResponse. Authentication required"},
        403: {"model": Error, "description": "You do not have enough rights to perform this operation"},
        4XX: {"model": Error, "description": "Client error"},
        "default": {"model": Error, "description": "Unexpected error"},
    },
    tags=["Payloads"],
    summary="List all payloads",
    response_model_by_alias=True,
)
async def get_all_payloads(
    offset: Optional[StrictInt] = Query(0, description="", alias="offset"),
    limit: Optional[StrictInt] = Query(5, description="", alias="limit"),
) -> GetAllPayloads200Response:
    """Use this endpoint to browse all payloads in the estimator."""
    if not BasePayloadsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BasePayloadsApi.subclasses[0]().get_all_payloads(offset, limit)


@router.get(
    "/payloads/{id}",
    responses={
        200: {"model": Payload, "description": "Payload Details"},
        401: {"model": Error, "description": "UnauthorizedResponse. Authentication required"},
        403: {"model": Error, "description": "You do not have enough rights to perform this operation"},
        404: {"model": Error, "description": "Resource not found"},
        4XX: {"model": Error, "description": "Client error"},
        "default": {"model": Error, "description": "Unexpected error"},
    },
    tags=["Payloads"],
    summary="Retrieve a payload by ID",
    response_model_by_alias=True,
)
async def get_payload(
    id: StrictInt = Path(..., description=""),
) -> Payload:
    """Use this endpoint to get the estimate for a specific route."""
    if not BasePayloadsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BasePayloadsApi.subclasses[0]().get_payload(id)


@router.put(
    "/payloads/{id}",
    responses={
        200: {"model": Payload, "description": "Payload Details"},
        401: {"model": Error, "description": "UnauthorizedResponse. Authentication required"},
        403: {"model": Error, "description": "You do not have enough rights to perform this operation"},
        404: {"model": Error, "description": "Resource not found"},
        4XX: {"model": Error, "description": "Client error"},
        "default": {"model": Error, "description": "Unexpected error"},
    },
    tags=["Payloads"],
    summary="Update payload with actuals.",
    response_model_by_alias=True,
)
async def update_payload(
    id: StrictInt = Path(..., description=""),
    payload: Annotated[Optional[Payload], Field(description="Payload Details")] = Body(None, description="Payload Details"),
) -> Payload:
    """Use this endpoint to update the payload with actuals."""
    if not BasePayloadsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BasePayloadsApi.subclasses[0]().update_payload(id, payload)
