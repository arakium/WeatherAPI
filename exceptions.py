from pydantic import ValidationError

class WeatherAPIError(Exception):
    """Base exception for weather API errors."""

    status_code = 500

    def __init__(self, errors: dict | str):
        self.errors = errors
        super().__init__(errors)


class InvalidParameterError(WeatherAPIError):
    """Exception raised when invalid parameters are provided."""

    status_code = 400

class CityNotFoundError(WeatherAPIError):

    status_code = 404

class APIConnectionError(WeatherAPIError):
    """Exception raised when connection to the weather API fails."""

    status_code = 503


class DataParsingError(WeatherAPIError):
    """Exception raised when the API response cannot be parsed."""

    status_code = 500


class RateLimitExceededError(WeatherAPIError):
    """Exception raised when the API rate limit is exceeded."""

    status_code = 429


def format_pydantic_errors(e: ValidationError) -> dict:
    """Turns Pydantic errors into a clean {field: message} dictionary."""
    return {
        "error":
            {
                str(err["loc"][0]):
                    err["msg"] for err in e.errors()
            }
    }