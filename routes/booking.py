from flask import Blueprint, request, jsonify
import logging

bp = Blueprint('booking', __name__)

@bp.route('/book-flight', methods=['POST'])
def book_flight():
    data = request.get_json(force=True)
    location = data.get('location', 'Unknown')
    date = data.get('date', 'Unspecified')

    logging.info(f"Received booking request: {data}")

    itinerary = {
        "location": location,
        "date": date,
        "flight": "Air Nigeria 101",
        "departure": "10:00 AM",
        "arrival": "12:30 PM"
    }

    logging.info(f"Returning itinerary: {itinerary}")
    return jsonify({
        "confirmation": "Flight booked!",
        "details": itinerary
    })
