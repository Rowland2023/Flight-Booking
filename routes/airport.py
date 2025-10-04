import requests
from flask import Blueprint, request, jsonify, current_app

bp = Blueprint('airport', __name__)

@bp.route('/airport', methods=['GET'])
def lookup_airport():
    city = request.args.get('city', '').strip()
    if not city:
        return jsonify({"error": "City parameter is required"}), 400

    # Get Amadeus access token
    token_url = 'https://test.api.amadeus.com/v1/security/oauth2/token'
    payload = {
        'grant_type': 'client_credentials',
        'client_id': current_app.config['AMADEUS_KEY'],
        'client_secret': current_app.config['AMADEUS_SECRET']
    }
    token_res = requests.post(token_url, data=payload)
    access_token = token_res.json().get('access_token')

    # Query airport data
    headers = { 'Authorization': f'Bearer {access_token}' }
    search_url = f'https://test.api.amadeus.com/v1/reference-data/locations?keyword={city}&subType=AIRPORT'
    res = requests.get(search_url, headers=headers)

    if res.status_code != 200:
        return jsonify({"error": "Failed to fetch airport data"}), 500

    data = res.json().get('data', [])
    airports = [{
        "name": a['name'],
        "iata": a['iataCode'],
        "city": a['address']['cityName'],
        "country": a['address']['countryName']
    } for a in data]

    return jsonify({"airports": airports})
