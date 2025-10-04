from flask import Blueprint, request, jsonify
import logging

bp = Blueprint('airport', __name__)

# Static airport data
AIRPORTS = [
    {"city": "lagos", "name": "Murtala Muhammed International Airport", "iata": "LOS", "country": "Nigeria"},
    {"city": "abuja", "name": "Nnamdi Azikiwe International Airport", "iata": "ABV", "country": "Nigeria"},
    {"city": "london", "name": "Heathrow Airport", "iata": "LHR", "country": "United Kingdom"},
    {"city": "new york", "name": "John F. Kennedy International Airport", "iata": "JFK", "country": "USA"},
    {"city": "tokyo", "name": "Narita International Airport", "iata": "NRT", "country": "Japan"}
]

@bp.route('/api/airport', methods=['GET'])
def lookup_airport():
    city = request.args.get('city', '').strip().lower()

    if not city:
        logging.warning("Airport lookup missing 'city' parameter.")
        return jsonify({"error": "City parameter is required"}), 400

    matches = [a for a in AIRPORTS if a['city'] == city]

    if matches:
        logging.info(f"✅ Airport lookup for '{city}': {matches}")
    else:
        logging.info(f"❌ No airport found for '{city}'")

    return jsonify({"airports": matches})
