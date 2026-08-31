from decimal import Decimal

from pydantic import BaseModel, Field


class CityRequest(BaseModel):
    city: str = Field(max_length=25)


class WeatherRequest(BaseModel):
    latitude: Decimal = Field(le=90, ge=-90)
    longitude: Decimal = Field(le=180, ge=-180)

class DailyWeather(BaseModel):
    time: list[str]
    temperature_max: list[float]
    temperature_min: list[float]


class WeatherResponse(BaseModel):
    city: str
    time: str
    humidity: int
    daily: DailyWeather
