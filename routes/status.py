from flask import Blueprint, request, jsonify
from amadeus import Client, ResponseError
import logging
import os

bp = Blueprint('status', __name__)

# Initialize Amadeus client securely
amadeus = Client(
    client_id=os.getenv('AMADEUS_KEY'),
    client_secret=os.getenv('AMADEUS_SECRET')
)

@bp.route('/status', methods=['GET'])
def get_flight_status():
    flight = request.args.get('flight', '').strip().upper()

    if not flight or len(flight) < 3:
        logging.warning("Flight status request missing or invalid 'flight' parameter.")
        return jsonify({"error": "Valid flight number is required"}), 400

    # Split flight into carrier and number (e.g. NG101 → NG + 101)
    carrier = ''.join(filter(str.isalpha, flight))
    number = ''.join(filter(str.isdigit, flight))
    date = request.args.get('date', '2025-10-05')  # Default or passed date

    try:
        response = amadeus.schedule.flights.get(
            carrierCode=carrier,
            flightNumber=number,
            scheduledDepartureDate=date
        )
        logging.info(f"Live flight status for {flight} on {date}: {response.data}")
        return jsonify({
            "flight": flight,
            "date": date,
            "status": response.data
        })
    except ResponseError as error:
        logging.error(f"Amadeus API error for {flight} on {date}: {error}")
        return jsonify({"error": "Unable to retrieve live flight status"}), 502
