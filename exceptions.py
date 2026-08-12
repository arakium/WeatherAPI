class WeatherAPIError(Exception):
    """Custom exception for weather API errors."""
    pass

class InvalidParameterError(WeatherAPIError):
    """Exception raised for invalid parameters."""
    status_code = 400

class APIConnectionError(WeatherAPIError):
    """Exception raised for API connection errors."""
    status_code = 503

class DataParsingError(WeatherAPIError):
    """Exception raised for errors in parsing the API response."""
    status_code = 500

class RateLimitExceededError(WeatherAPIError):
    """Exception raised when the API rate limit is exceeded."""
    status_code = 429
