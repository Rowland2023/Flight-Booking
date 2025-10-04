from flask import Blueprint, request, jsonify
import requests, logging, os

bp = Blueprint('weather', __name__)

WEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
WEATHER_URL = 'https://api.openweathermap.org/data/2.5/weather'

@bp.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city', '').strip()

    if not city:
        logging.warning("Weather request missing 'city' parameter.")
        return jsonify({"error": "City parameter is required"}), 400

    if not WEATHER_API_KEY:
        logging.error("Missing OpenWeather API key.")
        return jsonify({"error": "Server configuration error"}), 500

    params = {
        'q': city,
        'appid': WEATHER_API_KEY,
        'units': 'metric'
    }

    try:
        response = requests.get(WEATHER_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        weather = {
            "city": city.title(),
            "description": data['weather'][0]['description'].capitalize(),
            "temperature": round(data['main']['temp']),
            "condition": data['weather'][0]['main'],
            "humidity": data['main']['humidity'],
            "wind_speed": data['wind']['speed']
        }

        logging.info(f"✅ Weather data retrieved for '{city}': {weather}")
        return jsonify(weather)

    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error for '{city}': {http_err}")
        return jsonify({"error": "Invalid city or API error"}), 404

    except requests.exceptions.RequestException as req_err:
        logging.error(f"Request error for '{city}': {req_err}")
        return jsonify({"error": "Unable to fetch weather data"}), 502
