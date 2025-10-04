# routes/flight.py

from flask import Blueprint, request, jsonify
from amadeus import Client, ResponseError
import os
import logging

bp = Blueprint('flight', __name__)

# Initialize Amadeus client with environment variables
amadeus = Client(
    client_id=os.getenv('AMADEUS_KEY'),
    client_secret=os.getenv('AMADEUS_SECRET')
)

@bp.route('/flight/status', methods=['GET'])
def flight_status():
    carrier = request.args.get('carrier', '').upper()
    number = request.args.get('number', '').strip()
    date = request.args.get('date', '').strip()

    if not all([carrier, number, date]):
        logging.warning("Missing required flight parameters.")
        return jsonify({'error': 'Missing required parameters: carrier, number, date'}), 400

    try:
        response = amadeus.schedule.flights.get(
            carrierCode=carrier,
            flightNumber=number,
            scheduledDepartureDate=date
        )
        logging.info(f"Flight status for {carrier} {number} on {date}: {response.data}")
        return jsonify(response.data)

    except ResponseError as error:
        logging.error(f"Amadeus API error for {carrier} {number} on {date}: {error}")
        return jsonify({'error': 'Unable to retrieve flight status'}), 502
