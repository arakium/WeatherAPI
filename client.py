import requests

from exceptions import (
    APIConnectionError,
    DataParsingError,
    InvalidParameterError,
    RateLimitExceededError,
    WeatherAPIError,
)
example_response = {'latitude': 36.1875, 'longitude': 37.1875, 'generationtime_ms': 0.06902217864990234, 'utc_offset_seconds': 0, 'timezone': 'GMT', 'timezone_abbreviation': 'GMT', 'elevation': 400.0, 'current_units': {'time': 'iso8601', 'interval': 'seconds', 'relative_humidity_2m': '%'}, 'current': {'time': '2026-08-15T14:15', 'interval': 900, 'relative_humidity_2m': 37}, 'daily_units': {'time': 'iso8601', 'temperature_2m_max': '°C', 'temperature_2m_min': '°C'}, 'daily': {'time': ['2026-08-15', '2026-08-16', '2026-08-17', '2026-08-18', '2026-08-19', '2026-08-20', '2026-08-21'], 'temperature_2m_max': [35.4, 34.8, 33.7, 35.1, 36.4, 37.7, 39.8], 'temperature_2m_min': [23.7, 23.1, 21.8, 21.5, 21.9, 22.8, 24.1]}}

FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"

def __fetch_data(url: str, params: dict) -> dict:
    """Fetch weather data from the Open-Meteo API."""

    try:
        response = requests.get(
            url=url,
            params=params,
            timeout=10,
        )

        response.raise_for_status()

        try:
            return response.json()

        except requests.exceptions.JSONDecodeError as e:
            raise DataParsingError(
                {"error": "failed to parse API response"}
            ) from e

    except requests.exceptions.HTTPError as e:

        if response.status_code == 400:
            raise InvalidParameterError(
                {"error": "invalid parameters provided"}
            ) from e

        if response.status_code == 429:
            raise RateLimitExceededError(
                {"error": "rate limit exceeded"}
            ) from e

        raise WeatherAPIError(
            {
                "error": (
                    "weather API returned "
                    f"HTTP {response.status_code}"
                )
            }
        ) from e

    except requests.exceptions.RequestException as e:
        raise APIConnectionError(
            {"error": "failed to connect to weather API"}
        ) from e

def geocode(city: str) -> dict:
    """Fetches the given location's latitude and longitude."""
    return __fetch_data(
        GEOCODE_URL, {"name":city}
    )

def get_weather_data(params: dict) -> dict:
    """Fetches weather data for given latitude and longitude."""
    return __fetch_data(FORECAST_URL, params)





if __name__ == "__main__":
    print(get_weather_data(params = {
    "latitude": 12,
    "longitude": 12,
    "daily": "temperature_2m_max,temperature_2m_min",
    "timezone": "auto",
}))