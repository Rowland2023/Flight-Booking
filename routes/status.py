from flask import Blueprint, request, jsonify
import logging

bp = Blueprint('status', __name__)

@bp.route('/api/status', methods=['GET'])
def get_flight_status():
    flight = request.args.get('flight', '').strip().upper()

    STATUS = {
        "NG101": {
            "flight": "Air Nigeria 101",
            "departure": "10:00 AM",
            "arrival": "12:30 PM",
            "gate": "A5",
            "status": "On Time"
        },
        "BA202": {
            "flight": "British Airways 202",
            "departure": "2:00 PM",
            "arrival": "6:45 PM",
            "gate": "B12",
            "status": "Delayed"
        },
        "JL303": {
            "flight": "Japan Airlines 303",
            "departure": "9:00 AM",
            "arrival": "4:00 PM",
            "gate": "C7",
            "status": "Landed"
        }
    }

    info = STATUS.get(flight, {
        "flight": flight,
        "departure": "Unknown",
        "arrival": "Unknown",
        "gate": "Unknown",
        "status": "Not Found"
    })

    logging.info(f"Flight status for {flight}: {info}")
    return jsonify(info)
