import asyncio
import csv
import logging
from pathlib import Path
from typing import Iterable

import click
from dependency_injector.wiring import Provide, inject
from pydantic import UUID4

from sparkly.app.containers import SparklyContainer, init_main_container
from sparkly.app.domain import commands
from sparkly.app.seedwork.domain import exceptions
from sparkly.app.seedwork.service_layer import CommandBus

ROOT_DIR = Path(__file__).parent.parent.parent.parent.parent
logger = logging.Logger(__name__)


def read_csv(path: str) -> Iterable[commands.VehicleLog]:
    with open(ROOT_DIR / path, "r") as fp:
        reader = csv.DictReader(fp)
        for line in reader:
            log = commands.VehicleLog(
                timestamp=line["timestamp"],
                speed=int(line["speed"]) if line["speed"] != "NULL" else None,
                odometer=float(line["odometer"]),
                shift_state=line["shift_state"] if line["shift_state"] != "NULL" else None,
                state_of_charge=int(line["soc"]),
                elevation=int(line["elevation"]),
            )
            yield log


@inject
async def load_vehicle_logs(
    path: Path,
    bus: CommandBus = Provide[SparklyContainer.message_busses.command],
) -> None:
    vehicle_id = UUID4(path.stem)
    logs = list(read_csv(str(path)))

    cmd_create_vehicle = commands.AddVehicle(vehicle_id=vehicle_id)
    try:
        await bus.handle(message=cmd_create_vehicle)
    except Exception:
        pass

    for line_no, log in enumerate(logs, 1):
        cmd_load_logs = commands.AddVehicleLog(vehicle_id=vehicle_id, log=log)
        try:
            await bus.handle(message=cmd_load_logs)
        except exceptions.DomainValidationError as e:
            logger.error("Failed to insert log from file %s at line %s.\nError: %s", str(path), line_no, e)


@click.command()
@click.option(
    "--folder_path",
    prompt="Path to the folder containing vehicle logs, starting from root directory.",
    default="samples/vehicle_logs",
)
def main(folder_path: str):
    loop = asyncio.get_event_loop()
    full_path = ROOT_DIR / folder_path
    for path in full_path.glob("*.csv"):
        loop.run_until_complete(load_vehicle_logs(path=path))


if __name__ == "__main__":
    container = init_main_container(modules=[__name__])
    main()
