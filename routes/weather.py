import requests
from flask import Blueprint, request, jsonify, current_app

bp = Blueprint('weather', __name__)

@bp.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    api_key = current_app.config['OPENWEATHER_API_KEY']
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'

    res = requests.get(url)
    if res.status_code != 200:
        return jsonify({'error': 'Weather data not found'}), 404

    data = res.json()
    return jsonify({
        'city': city,
        'description': data['weather'][0]['description'].title(),
        'temperature': data['main']['temp'],
        'condition': data['weather'][0]['main'],
        'humidity': data['main']['humidity'],
        'wind_speed': data['wind']['speed']
    })
