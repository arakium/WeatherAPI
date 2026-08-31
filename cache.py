import os
import redis
from dotenv import load_dotenv
from services import get_city_weather
from model import WeatherResponse

def get_redis_url() -> str:
    load_dotenv()
    redis_url = os.getenv("REDIS_URL")

    if not redis_url:
        raise RuntimeError("REDIS_URL environment variable is not set")

    return redis_url

redis_client = redis.Redis.from_url(get_redis_url())

def get_cached_data(city: str):
    cache_key = f"weather_data:{city.lower()}"
    cached_data = redis_client.get(cache_key)
    if cached_data:
        return WeatherResponse.model_validate_json(cached_data)

    weather = get_city_weather(city)

    serialized = weather.model_dump_json()

    redis_client.setex(
        cache_key,
        43200,
        serialized
    )
    return weather

