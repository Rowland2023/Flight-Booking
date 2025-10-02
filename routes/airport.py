from flask import Blueprint, request, jsonify
import logging

bp = Blueprint('airport', __name__)

@bp.route('/api/airport', methods=['GET'])
def lookup_airport():
    city = request.args.get('city', '').strip().lower()

    AIRPORTS = [
        {"city": "lagos", "name": "Murtala Muhammed International Airport", "iata": "LOS", "country": "Nigeria"},
        {"city": "abuja", "name": "Nnamdi Azikiwe International Airport", "iata": "ABV", "country": "Nigeria"},
        {"city": "london", "name": "Heathrow Airport", "iata": "LHR", "country": "United Kingdom"},
        {"city": "new york", "name": "John F. Kennedy International Airport", "iata": "JFK", "country": "USA"},
        {"city": "tokyo", "name": "Narita International Airport", "iata": "NRT", "country": "Japan"}
    ]

    matches = [a for a in AIRPORTS if a['city'] == city]
    logging.info(f"Airport lookup for {city}: {matches}")
    return jsonify({"airports": matches})
