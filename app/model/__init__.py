import json
from datetime import datetime
from enum import Enum

from flask.json import JSONEncoder


class MeasurementUnit(str, Enum):
    kWh = "kWh"
    mWh = "mWh"
    m3 = "m3"


class Measurement:
    def __init__(self, reading: float, unit: MeasurementUnit, time: datetime, contract: str, photo: str):
        self.reading = reading
        self.unit = unit
        self.time = time
        self.contract = contract
        self.photo = photo


class MeasurementEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

