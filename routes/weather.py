from flask import Blueprint, request, jsonify
import requests, logging
from config import WEATHER_API_KEY, WEATHER_URL

bp = Blueprint('weather', __name__)

@bp.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city', '').strip()
    if not city:
        logging.warning("Weather request missing 'city' parameter.")
        return jsonify({"error": "City parameter is required"}), 400

    params = {
        'q': city,
        'appid': WEATHER_API_KEY,
        'units': 'metric'
    }

    try:
        response = requests.get(WEATHER_URL, params=params)
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

        logging.info(f"Weather data retrieved for {city}: {weather}")
        return jsonify(weather)

    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error for {city}: {http_err}")
        return jsonify({"error": "Invalid city or API error"}), 404
    except requests.exceptions.RequestException as req_err:
        logging.error(f"Request error for {city}: {req_err}")
        return jsonify({"error": "Unable to fetch weather data"}), 500
