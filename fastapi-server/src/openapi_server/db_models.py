from sqlalchemy import Column, Integer, String, Float, MetaData, Table
from sqlalchemy.orm import registry

mapper_registry = registry()
metadata = MetaData()

payloads_table = Table(
    "payloads",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("origin", String(8), nullable=True),
    Column("destination", String(8), nullable=True),
    Column("julian_do_y", Integer, nullable=True),
    Column("passengers", Integer, nullable=True),
    Column("baggage", Float, nullable=True),
    Column("cargo", Float, nullable=True),
)


class PayloadORM:
    def __init__(
        self,
        id: int = None,
        origin: str | None = None,
        destination: str | None = None,
        julian_do_y: int | None = None,
        passengers: int | None = None,
        baggage: float | None = None,
        cargo: float | None = None,
    ):
        self.id = id
        self.origin = origin
        self.destination = destination
        self.julian_do_y = julian_do_y
        self.passengers = passengers
        self.baggage = baggage
        self.cargo = cargo


mapper_registry.map_imperatively(PayloadORM, payloads_table)
