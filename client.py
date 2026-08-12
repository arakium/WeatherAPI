import requests

from exceptions import DataParsingError, APIConnectionError, WeatherAPIError, RateLimitExceededError, \
    InvalidParameterError

URL = "https://api.open-meteo.com/v1/forecast"

def get_weather_data(params: dict) -> dict:
    """Fetch weather data from the Open-Meteo API."""
    try:
        response = requests.get(URL, params=params)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.HTTPError as e:
        if response.status_code == 400:
            raise InvalidParameterError(
                f"Invalid parameter provided."
            )
        elif response.status_code == 429:
            raise RateLimitExceededError(
                f"Rate limit exceeded."
            )
        else:
            raise WeatherAPIError(
                f"ERROR: {response.status_code}"
            )

    except requests.exceptions.JSONDecodeError as e:
        raise DataParsingError(
            f"Failed to parse API response."
        )

    except requests.exceptions.RequestException as e:
        raise APIConnectionError(
            f"Failed to connect to weather API."
        )


print(get_weather_data({"latitude":36.138650, "longitude": 36.823919, "daily": "temperature_2m_max,temperature_2m_min", "timezone": "auto"}))