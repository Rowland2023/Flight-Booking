import requests
from flask import Blueprint, request, jsonify, current_app

bp = Blueprint('dashboard', __name__)

def get_amadeus_token():
    token_url = 'https://test.api.amadeus.com/v1/security/oauth2/token'
    payload = {
        'grant_type': 'client_credentials',
        'client_id': current_app.config['AMADEUS_CLIENT_ID'],
        'client_secret': current_app.config['AMADEUS_CLIENT_SECRET']
    }
    res = requests.post(token_url, data=payload)
    if res.status_code != 200:
        current_app.logger.error(f"❌ Amadeus token failed: {res.text}")
        return None
    return res.json().get('access_token')

@bp.route('/dashboard', methods=['GET'])
def get_dashboard():
    location = request.args.get('location', 'Unknown').title()
    date = request.args.get('date', 'Unspecified')
    flight = request.args.get('flight', 'NG101').upper()

    # 🌤️ Fetch weather
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={current_app.config['OPENWEATHER_API_KEY']}&units=metric"
    weather_res = requests.get(weather_url)
    weather_data = weather_res.json() if weather_res.ok else {}
    weather_summary = f"{weather_data.get('weather', [{}])[0].get('description', 'Unknown')}, {weather_data.get('main', {}).get('temp', 'N/A')}°C"

    # 🛫 Fetch airport info
    token = get_amadeus_token()
    if not token:
        return jsonify({"error": "Failed to retrieve Amadeus token"}), 502

    headers = { 'Authorization': f'Bearer {token}' }
    airport_url = f"https://test.api.amadeus.com/v1/reference-data/locations?keyword={location}&subType=AIRPORT"
    airport_res = requests.get(airport_url, headers=headers)
    airport_data = airport_res.json().get('data', []) if airport_res.ok else []
    airport_summary = airport_data[0]['name'] + f" ({airport_data[0]['iataCode']})" if airport_data else "No airport found"

    # 💡 Fetch travel tips
    tips_url = f"{current_app.config.get('FLASK_URL', 'http://localhost:5000')}/api/tips?city={location}"
    tips_res = requests.get(tips_url)
    tips_data = tips_res.json() if tips_res.ok else {}
    tips_summary = (
        f"🧳 {tips_data.get('packing', 'No packing advice')}\n"
        f"🛂 {tips_data.get('visa', 'Visa info unavailable')}\n"
        f"🛡️ {tips_data.get('safety', 'No safety tips')}"
    )

    # 📡 Fetch flight status
    status_url = f"{current_app.config.get('FLASK_URL', 'http://localhost:5000')}/api/status?flight={flight}"
    status_res = requests.get(status_url)
    status_data = status_res.json() if status_res.ok else {}
    status_summary = status_data.get('status', f"✈️ Flight {flight} status unavailable.")

    # 📊 Final dashboard summary
    summary = {
        "location": location,
        "date": date,
        "flight": flight,
        "weather": weather_summary,
        "airport": airport_summary,
        "tips": tips_summary,
        "status": status_summary
    }

    return jsonify(summary)
