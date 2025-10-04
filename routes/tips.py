import requests
from flask import Blueprint, request, jsonify, current_app

bp = Blueprint('tips', __name__)

def get_amadeus_token():
    url = 'https://test.api.amadeus.com/v1/security/oauth2/token'
    payload = {
        'grant_type': 'client_credentials',
        'client_id': current_app.config['AMADEUS_CLIENT_ID'],
        'client_secret': current_app.config['AMADEUS_CLIENT_SECRET']
    }
    res = requests.post(url, data=payload)
    if res.status_code != 200:
        current_app.logger.error(f"❌ Amadeus token failed: {res.text}")
        return None
    return res.json().get('access_token')

@bp.route('/tips', methods=['GET'])
def get_tips():
    city = request.args.get('city', '').title()
    if not city:
        return jsonify({'error': 'City parameter is required'}), 400

    token = get_amadeus_token()
    if not token:
        return jsonify({'error': 'Failed to retrieve Amadeus token'}), 502

    headers = { 'Authorization': f'Bearer {token}' }

    # Placeholder: Amadeus does not have a travel tips endpoint
    # Simulate tips based on city name
    tips_db = {
        "London": {
            "packing": "Pack layers and a raincoat.",
            "visa": "UK visa required for Nigerian passport holders.",
            "safety": "Stay alert in crowded areas.",
            "etiquette": "Queue patiently and avoid loud conversations."
        },
        "Lagos": {
            "packing": "Light clothing and mosquito repellent.",
            "visa": "No visa needed for Nigerian citizens.",
            "safety": "Avoid isolated areas after dark.",
            "etiquette": "Greet elders respectfully and be punctual."
        }
    }

    tips = tips_db.get(city)
    if not tips:
        return jsonify({'error': f'No travel tips available for {city}'}), 404

    return jsonify(tips)
