from flask import Blueprint, request, jsonify
import logging

bp = Blueprint('dashboard', __name__)

@bp.route('/dashboard', methods=['GET'])
def get_dashboard():
    location = request.args.get('location', 'Unknown').title()
    date = request.args.get('date', 'Unspecified')
    flight = request.args.get('flight', 'NG101').upper()

    summary = {
        "location": location,
        "date": date,
        "flight": flight,
        "weather": "Sunny, 28°C",
        "airport": "Murtala Muhammed International Airport (LOS)",
        "tips": (
            "🧳 Pack light clothes and mosquito repellent.\n"
            "🛂 Visa required.\n"
            "🛡️ Avoid late-night travel."
        ),
        "status": f"✈️ Flight {flight} is On Time. Gate A5. Departure 10:00 AM."
    }

    logging.info(f"Dashboard summary for {location} on {date}: {summary}")
    return jsonify(summary)
