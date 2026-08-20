from __future__ import annotations

import random
from typing import Final

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

WEATHER_CONDITIONS: Final[tuple[str, ...]] = ("晴れ", "くもり", "雨", "雪")
MIN_TEMPERATURE: Final[int] = -10
MAX_TEMPERATURE: Final[int] = 35


class WeatherResponse(BaseModel):
    region: str
    forecast: str


def generate_forecast(region: str) -> WeatherResponse:
    normalized_region = region.strip()
    if not normalized_region:
        raise ValueError("region must not be blank")

    condition = random.choice(WEATHER_CONDITIONS)
    temperature = random.randint(MIN_TEMPERATURE, MAX_TEMPERATURE)
    return WeatherResponse(
        region=normalized_region,
        forecast=f"{condition}、{temperature}℃",
    )


app = FastAPI(title="Weather Forecast API")


@app.get("/", tags=["health"])
def read_root() -> dict[str, str]:
    return {"message": "Use /weather/{region} to get a forecast."}


@app.get("/weather/{region}", response_model=WeatherResponse, tags=["weather"])
def read_weather(region: str) -> WeatherResponse:
    try:
        return generate_forecast(region)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
