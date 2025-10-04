import requests
from flask import Blueprint, request, jsonify, current_app
from requests.exceptions import RequestException

bp = Blueprint('airport', __name__)

# --- Reusable Core Logic ---
# Function to get Amadeus Token (needed by airport, tips, booking)
# It's best practice to put this in a shared utility file, but we'll include it here
# and import it in tips.py for simplicity.
def get_amadeus_token():
    """Fetches a new Amadeus access token."""
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


def lookup_airport_data(city: str) -> tuple:
    """Fetches airport data from Amadeus. Reusable by other internal routes."""
    token = get_amadeus_token()
    if not token:
        return {"error": "Failed to retrieve Amadeus token"}, 502

    headers = { 'Authorization': f'Bearer {token}' }
    search_url = f'https://test.api.amadeus.com/v1/reference-data/locations?keyword={city}&subType=AIRPORT'
    
    try:
        res = requests.get(search_url, headers=headers, timeout=10)
        res.raise_for_status()
        
        data = res.json().get('data', [])
        
        if not data:
            return {"error": f"No airport found for {city}"}, 404
        
        airports = [{
            "name": a['name'],
            "iata": a['iataCode'],
            "city": a['address']['cityName'],
            # The key is 'countryName' in your example, but using 'country' for simplicity
            "country": a['address']['countryName'] 
        } for a in data]

        return {"airports": airports}, 200

    except RequestException as e:
        current_app.logger.error(f"❌ Amadeus Airport Request failed for {city}: {e}. Response: {getattr(res, 'text', 'N/A')}")
        return {"error": "External API connection failure"}, 503
    except Exception as e:
        current_app.logger.critical(f"Airport lookup internal error: {e}", exc_info=True)
        return {"error": "Internal server error during lookup"}, 500


# --- Public API Route ---
@bp.route('/api/airport', methods=['GET'])
def lookup_airport():
    city = request.args.get('city', '').strip()
    if not city:
        return jsonify({"error": "City parameter is required"}), 400

    data, status = lookup_airport_data(city)
    return jsonify(data), status