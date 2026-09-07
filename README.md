<a id="readme-top"></a>

## WeatherAPI

A lightweight Flask-based REST API that fetches and normalizes weather data from external providers (Open-Meteo). It
provides endpoints for current weather and short forecasts and caches responses in Redis.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Table of Contents

- About The Project
- Built With
- Getting Started
    - Prerequisites
    - Installation
- Usage
- Contact
- Acknowledgments

## About The Project

WeatherAPI handles client requests for weather data, validates parameters with Pydantic models, resolves city
coordinates via a geocoding API, requests forecast data from Open-Meteo, and caches normalized responses in Redis for
improved latency and reduced provider calls.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

- Python 3.10+
- Flask
- Flask-Limiter (rate limiting)
- Redis (cache)
- Requests
- Pydantic
- Gunicorn
- Nginx

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started

### Prerequisites

- Python 3.10 or later
- Redis server reachable from the app
- An internet connection to reach Open-Meteo geocoding and forecast endpoints

### Installation

1. Clone the repo and enter the directory:

```sh
git clone https://github.com/arakium/WeatherAPI.git
cd WeatherAPI
```

2. Create and activate a virtual environment:

```sh
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:

```sh
pip install -r requirements.txt
```

4. Configure environment variables (example):

```sh
export REDIS_URL="redis://localhost:6379"
```

5. Start Gunicorn:

```sh
gunicorn -w 4 -b 127.0.0.1:8000 app:app --reload
```

6. Start Nginx to work as reverse proxy and enable it on boot:

```sh
sudo systemctl enable --now nginx
```

(For local development you can also use Flask's runner: `FLASK_APP=app.py flask run`.)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Usage

Endpoints:

- GET /weather?city=<city_name>
    - Returns normalized current weather and short daily forecasts for the requested city.

Example:

```sh
curl "http://localhost:8000/weather?city=Aleppo"
```

Response shape (example):

```json
{
  "city": "aleppo",
  "daily": {
    "temperature_max": [
      33.8,
      35.1,
      35.2,
      36.1,
      37.5,
      38.4,
      39.0
    ],
    "temperature_min": [
      21.1,
      18.8,
      20.3,
      21.5,
      22.0,
      22.4,
      21.9
    ],
    "time": [
      "2026-09-08",
      "2026-09-09",
      "2026-09-10",
      "2026-09-11",
      "2026-09-12",
      "2026-09-13",
      "2026-09-14"
    ]
  },
  "humidity": 28,
  "time": "2026-09-08T01:00"
}
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contact

Project maintainer: arakium — https://github.com/arakium

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<p align="right">(<a href="#readme-top">back to top</a>)</p>
