import httpx
import pytest

from main import (
    MAX_TEMPERATURE,
    MIN_TEMPERATURE,
    WEATHER_CONDITIONS,
    app,
    generate_forecast,
)


def test_generate_forecast_uses_random_values(monkeypatch):
    monkeypatch.setattr("main.random.choice", lambda values: values[0])
    monkeypatch.setattr("main.random.randint", lambda start, end: 20)

    forecast = generate_forecast("東京")

    assert forecast.region == "東京"
    assert forecast.forecast == "晴れ、20℃"


def test_generate_forecast_rejects_blank_region():
    try:
        generate_forecast("   ")
    except ValueError as error:
        assert str(error) == "region must not be blank"
    else:
        raise AssertionError("ValueError was not raised")


@pytest.mark.anyio
async def test_weather_endpoint_returns_forecast():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://testserver",
    ) as client:
        response = await client.get("/weather/東京")

    assert response.status_code == 200
    payload = response.json()
    assert payload["region"] == "東京"
    condition, temperature = payload["forecast"].split("、")
    assert condition in WEATHER_CONDITIONS
    assert temperature.endswith("℃")
    value = int(temperature[:-1])
    assert MIN_TEMPERATURE <= value <= MAX_TEMPERATURE
