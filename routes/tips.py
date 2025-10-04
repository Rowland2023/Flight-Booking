from flask import Blueprint, request, jsonify, current_app
# ⬅️ IMPORT the core lookup function from the airport module
from .airport import lookup_airport_data, get_amadeus_token

bp = Blueprint('tips', __name__)

@bp.route('/api/tips', methods=['GET'])
def get_tips():
    city = request.args.get('city', '').title()
    if not city:
        return jsonify({'error': 'City parameter is required'}), 400

    # ⬅️ INTERNAL CALL: Call the Python function directly
    airport_data, status = lookup_airport_data(city)

    # If airport lookup failed (e.g., 502, 404, 503), return that status directly
    if status != 200 or not airport_data.get('airports'):
        return jsonify(airport_data), status 

    city_info = airport_data['airports'][0] # Use the first match
    country = city_info.get('country', 'Unknown')
    current_app.logger.info(f"🌍 Generating tips for {city}, {country}")

    # Dynamic tip generation logic...
    tips = {
        "packing": "Pack essentials and check the weather forecast.",
        "visa": f"Check visa requirements for travel to {country}.",
        "safety": "Stay aware of your surroundings and follow local guidelines.",
        "etiquette": f"Respect cultural norms in {country}, especially around dress and greetings."
    }

    # Optional: Country-specific overrides
    if country == "France":
        tips["etiquette"] = "Greet with 'Bonjour', avoid loud conversations, and respect personal space."
    elif country == "Nigeria":
        tips["safety"] = "Avoid isolated areas after dark and stay hydrated."
        tips["etiquette"] = "Greet elders respectfully and be mindful of local customs."

    return jsonify(tips)