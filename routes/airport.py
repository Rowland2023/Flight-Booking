import requests
from flask import Blueprint, request, jsonify, current_app

bp = Blueprint('airport', __name__)

def get_amadeus_token():
    token_url = 'https://test.api.amadeus.com/v1/security/oauth2/token'
    payload = {
        'grant_type': 'client_credentials',
        'client_id': current_app.config['AMADEUS_CLIENT_ID'],
        'client_secret': current_app.config['AMADEUS_CLIENT_SECRET']
    }
    res = requests.post(token_url, data=payload)
    if res.status_code != 200:
        current_app.logger.error(f"❌ Amadeus token request failed: {res.text}")
        return None
    return res.json().get('access_token')

@bp.route('/airport', methods=['GET'])
def lookup_airport():
    city = request.args.get('city', '').strip()
    if not city:
        return jsonify({"error": "City parameter is required"}), 400

    token = get_amadeus_token()
    if not token:
        return jsonify({"error": "Failed to retrieve Amadeus token"}), 502

    headers = { 'Authorization': f'Bearer {token}' }
    search_url = f'https://test.api.amadeus.com/v1/reference-data/locations?keyword={city}&subType=AIRPORT'
    res = requests.get(search_url, headers=headers)

    if res.status_code != 200:
        current_app.logger.error(f"❌ Airport lookup failed for '{city}': {res.text}")
        return jsonify({"error": "Failed to fetch airport data"}), 500

    data = res.json().get('data', [])
    if not data:
        return jsonify({"error": f"No airport found for '{city}'"}), 404

    airports = [{
        "name": a['name'],
        "iata": a['iataCode'],
        "city": a['address']['cityName'],
        "country": a['address']['countryName']
    } for a in data]

    return jsonify({"airports": airports})
