import logging
from flask import Flask, request
from flask_limiter import Limiter, RateLimitExceeded
from flask_limiter.util import get_remote_address
from pydantic import ValidationError as PydanticValidationError

from model import WeatherRequest, CityRequest
from cache import get_cached_data, get_redis_url
from exceptions import WeatherAPIError, format_pydantic_errors

logger = logging.getLogger(__name__)
app = Flask(__name__)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["10 per hour"],
    storage_uri=get_redis_url(),
    storage_options={"socket_connect_timeout": 30},
    strategy="sliding-window-counter",  # Options: "fixed-window", "moving-window", or "sliding-window-counter"
)


@app.errorhandler(WeatherAPIError)
def handle_weather_api_error(error):
    return {
        "errors": error.errors
    }, error.status_code


@app.errorhandler(PydanticValidationError)
def handle_pydantic_error(error):
    return format_pydantic_errors(error), 400

@app.errorhandler(RateLimitExceeded)
def handle_rate_limit(error):
    return {
        "error": "rate limit exceeded"
    }, 429

@app.errorhandler(Exception)
def handle_unexpected_error(error):
    logger.exception("Unexpected error")
    return {
        "error": "internal server error"
    }, 500


@app.get("/weather")
def weather():
    city = request.args.get("city")

    requested_city = CityRequest(city=city)

    return get_cached_data(requested_city.city).model_dump()
