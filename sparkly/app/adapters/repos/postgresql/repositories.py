from sparkly.app.domain import entities
from sparkly.app.seedwork import adapters


class VehicleLogsRepository(adapters.SQLAlchemyRepository[entities.Vehicle]):
    pass
