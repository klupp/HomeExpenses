from enum import Enum
from typing import List

from fastapi import FastAPI
from pydantic import (
	BaseModel,
	PositiveFloat,
	PositiveInt,
	AwareDatetime,
	FilePath,
	model_validator
)


class MeasurementType(
	str,
	Enum
):
	gas = "gas"
	electricity = "electricity"
	water = "water"


class MeasurementUnit(
	str,
	Enum
):
	kWh = "kWh"
	mWh = "mWh"
	m3 = "m3"


ALLOWED_UNITS = {
	MeasurementType.gas: {
		MeasurementUnit.kWh,
		MeasurementUnit.mWh,
		MeasurementUnit.m3
	},
	MeasurementType.electricity: {
		MeasurementUnit.kWh,
		MeasurementUnit.mWh
	},
	MeasurementType.water: {
		MeasurementUnit.m3
	},
}


class MeasurementCreate(
	BaseModel
):
	contract_id: PositiveInt
	date: AwareDatetime
	type: MeasurementType
	unit: MeasurementUnit
	aggregate_consumption: PositiveFloat
	photo: FilePath | None = None

	@model_validator(
		mode='after'
	)
	def check_unit_matches_type(
			self
	):
		allowed_units = ALLOWED_UNITS.get(
			self.type,
			set()
		)
		if self.unit not in allowed_units:
			raise ValueError(
				f"Unit '{self.unit}' is not valid for measurement type '{self.type}'."
			)
		return self


class Measurement(
	MeasurementCreate
):
	id: PositiveInt


async def measurements_dummy_db() -> List[Measurement]:
	return [
		Measurement(
			id=1,
			contract_id=1,
			date="2019-05-11T12:34:05.743146Z",
			type=MeasurementType.gas,
			unit=MeasurementUnit.m3,
			aggregate_consumption=300,
			photo="app/static/uploads/20211102_143758.jpg"
		)
	]


app = FastAPI()


@app.get(
	"/measurements",
	response_model=List[Measurement]
)
async def get_measurements() -> List[Measurement]:
	return await measurements_dummy_db()


@app.post(
	"/measurements",
	response_model=Measurement
)
async def create_measurement(
		measurement: MeasurementCreate
) -> Measurement:
	return Measurement(
		id=10,
		**measurement.model_dump()
	)
