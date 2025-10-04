from flask import Blueprint, request, jsonify
import logging

bp = Blueprint('booking', __name__)

@bp.route('/api/book-flight', methods=['POST'])
def book_flight():
    try:
        data = request.get_json(force=True)
        location = data.get('location', '').title() or 'Unknown'
        date = data.get('date', '') or 'Unspecified'

        logging.info(f"📨 Received booking request: {data}")

        itinerary = {
            "location": location,
            "date": date,
            "flight": "Air Nigeria 101",
            "departure": "10:00 AM",
            "arrival": "12:30 PM"
        }

        logging.info(f"✅ Returning itinerary: {itinerary}")
        return jsonify({
            "confirmation": f"Flight to {location} booked for {date}!",
            "details": itinerary
        })

    except Exception as e:
        logging.error(f"❌ Booking error: {e}")
        return jsonify({"error": "Failed to process booking"}), 500
