import requests
from flask import Blueprint, request, jsonify, current_app

bp = Blueprint('dashboard', __name__)

def get_amadeus_token():
    token_url = 'https://test.api.amadeus.com/v1/security/oauth2/token'
    payload = {
        'grant_type': 'client_credentials',
        'client_id': current_app.config['AMADEUS_KEY'],
        'client_secret': current_app.config['AMADEUS_SECRET']
    }
    res = requests.post(token_url, data=payload)
    return res.json().get('access_token')

@bp.route('/dashboard', methods=['GET'])
def get_dashboard():
    location = request.args.get('location', 'Unknown').title()
    date = request.args.get('date', 'Unspecified')
    flight = request.args.get('flight', 'NG101').upper()

    # Fetch weather
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={current_app.config['OPENWEATHER_API_KEY']}&units=metric"
    weather_res = requests.get(weather_url)
    weather_data = weather_res.json() if weather_res.ok else {}

    # Fetch airport info
    token = get_amadeus_token()
    headers = { 'Authorization': f'Bearer {token}' }
    airport_url = f"https://test.api.amadeus.com/v1/reference-data/locations?keyword={location}&subType=AIRPORT"
    airport_res = requests.get(airport_url, headers=headers)
    airport_data = airport_res.json().get('data', []) if airport_res.ok else []

    # Fetch travel tips
    tips_url = f"{current_app.config.get('FLASK_URL', 'http://localhost:5000')}/api/tips?city={location}"
    tips_res = requests.get(tips_url)
    tips_data = tips_res.json() if tips_res.ok else {}

    # Fetch flight status (mocked or real)
    status_url = f"{current_app.config.get('FLASK_URL', 'http://localhost:5000')}/api/status?flight={flight}"
    status_res = requests.get(status_url)
    status_data = status_res.json() if status_res.ok else {}

    summary = {
        "location": location,
        "date": date,
        "flight": flight,
        "weather": f"{weather_data.get('description', 'Unknown')}, {weather_data.get('temperature', 'N/A')}°C",
        "airport": airport_data[0]['name'] + f" ({airport_data[0]['iataCode']})" if airport_data else "No airport found",
        "tips": (
            f"🧳 {tips_data.get('packing', 'No packing advice')}\n"
            f"🛂 {tips_data.get('visa', 'Visa info unavailable')}\n"
            f"🛡️ {tips_data.get('safety', 'No safety tips')}"
        ),
        "status": status_data.get('status', f"✈️ Flight {flight} status unavailable.")
    }

    return jsonify(summary)
