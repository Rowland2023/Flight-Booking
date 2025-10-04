import requests
import logging # Import logging if not already done
from flask import Blueprint, request, jsonify, current_app
from requests.exceptions import RequestException # Import for error handling

bp = Blueprint('weather', __name__)

@bp.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city', '').strip()
    
    # 1. Input Validation
    if not city:
        current_app.logger.warning("Weather request missing 'city' parameter.")
        return jsonify({'error': 'City parameter is required'}), 400

    api_key = current_app.config.get('OPENWEATHER_API_KEY')
    
    # 2. Configuration Validation
    if not api_key:
        current_app.logger.error("❌ OPENWEATHER_API_KEY is missing.")
        return jsonify({'error': 'Server configuration error'}), 500

    weather_url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }

    try:
        # 3. Robust API Request with Timeout
        res = requests.get(weather_url, params=params, timeout=10)
        res.raise_for_status() # Handles 4xx and 5xx responses from OpenWeather

        data = res.json()
        
        # 4. Error Handling for City Not Found (Specific 404/400)
        if data.get('cod') == '404':
             current_app.logger.info(f"Weather data not found for city: {city}")
             return jsonify({'error': f'City "{city}" not found'}), 404

        return jsonify({
            'city': data.get('name', city),
            'description': data['weather'][0]['description'].title(),
            'temperature': data['main']['temp'],
            'condition': data['weather'][0]['main'],
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed']
        })

    except requests.exceptions.HTTPError as http_err:
        # Handles 401, 429, 500 from OpenWeather (e.g., bad API key, limit exceeded)
        current_app.logger.error(f"HTTP error for '{city}': {http_err}. Response: {res.text}")
        return jsonify({'error': 'External API access issue'}), res.status_code
        
    except RequestException as req_err:
        # Handles connection issues (DNS, timeout, etc.)
        current_app.logger.error(f"Connection error for '{city}': {req_err}")
        return jsonify({'error': 'Unable to connect to weather service'}), 503
    
    except KeyError as key_err:
        # Handles unexpected JSON structure (e.g., if a key like 'main' is missing)
        current_app.logger.error(f"Data parsing error for '{city}': {key_err}. Response: {data}")
        return jsonify({'error': 'Unexpected weather data format'}), 500