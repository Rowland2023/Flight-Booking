from flask import Blueprint, request, jsonify
import logging

bp = Blueprint('dashboard', __name__)

@bp.route('/api/dashboard', methods=['GET'])
def get_dashboard():
    location = request.args.get('location', 'Unknown')
    date = request.args.get('date', 'Unspecified')
    flight = request.args.get('flight', 'NG101')

    summary = {
        "location": location,
        "date": date,
        "flight": flight,
        "weather": "Sunny, 28°C",
        "airport": "Murtala Muhammed International Airport (LOS)",
        "tips": "Pack light clothes and mosquito repellent. Visa required. Avoid late-night travel.",
        "status": "Flight NG101 is On Time. Gate A5. Departure 10:00 AM."
    }

    logging.info(f"Dashboard summary for {location} on {date}: {summary}")
    return jsonify(summary)
