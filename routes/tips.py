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

def get_city_info(city):
    try:
        res = requests.get(f"{request.host_url}api/airport?city={city}", timeout=5)
        if res.status_code == 200:
            airports = res.json().get('airports', [])
            if airports:
                return airports[0]
    except Exception as e:
        current_app.logger.error(f"❌ City info lookup failed for {city}: {e}")
    return None

@bp.route('/tips', methods=['GET'])
def get_tips():
    city = request.args.get('city', '').title()
    if not city:
        return jsonify({'error': 'City parameter is required'}), 400

    token = get_amadeus_token()
    if not token:
        return jsonify({'error': 'Failed to retrieve Amadeus token'}), 502

    city_info = get_city_info(city)
    if not city_info:
        current_app.logger.warning(f"⚠️ No airport info found for {city}")
        return jsonify({
            "message": f"No specific tips for {city}. Showing general advice.",
            "tips": {
                "packing": "Pack essentials and check the weather forecast.",
                "visa": "Check visa requirements before traveling.",
                "safety": "Stay aware of your surroundings.",
                "etiquette": "Respect local customs and dress codes."
            }
        }), 200

    country = city_info.get('countryName', 'Unknown')
    current_app.logger.info(f"🌍 Generating tips for {city}, {country}")

    tips = {
        "packing": "Pack essentials and check the weather forecast.",
        "visa": f"Check visa requirements for travel to {country}.",
        "safety": "Stay aware of your surroundings and follow local guidelines.",
        "etiquette": f"Respect cultural norms in {country}, especially around dress and greetings."
    }

    if country == "France":
        tips["etiquette"] = "Greet with 'Bonjour', avoid loud conversations, and respect personal space."
    elif country == "Nigeria":
        tips["safety"] = "Avoid isolated areas after dark and stay hydrated."
        tips["etiquette"] = "Greet elders respectfully and be mindful of local customs."

    return jsonify(tips)
