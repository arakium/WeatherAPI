from client import get_weather_data, geocode
from exceptions import CityNotFoundError, DataParsingError
from model import WeatherRequest, WeatherResponse, DailyWeather


def get_city_coordinates(city: str) -> dict:
    data = geocode(city)

    try:
        result = data["results"][0]
        return {
            "latitude": result["latitude"],
            "longitude": result["longitude"],
        }

    except (IndexError, KeyError) as e:
        raise CityNotFoundError(
            {
                "error": f"city (${city}) not found"
            }
        ) from e

def get_city_weather(city: str) -> WeatherResponse:
    response = get_city_coordinates(city)
    coordinates = WeatherRequest(**response).model_dump()
    response = get_weather_data(
        {
            **coordinates,
            "daily": "temperature_2m_max,temperature_2m_min",
            "current": "relative_humidity_2m",
            "timezone": "auto"
        }
    )
    daily = DailyWeather(
        time=response["daily"]["time"],
        temperature_max=response["daily"]["temperature_2m_max"],
        temperature_min=response["daily"]["temperature_2m_min"],
    )

    return WeatherResponse(
        city=city,
        time=response["current"]["time"],
        humidity=response["current"]["relative_humidity_2m"],
        daily=daily,
    )

if __name__ == "__main__":
    print(get_city_weather("Atareb").model_dump())