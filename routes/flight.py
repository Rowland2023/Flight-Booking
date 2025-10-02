# routes/flight.py
from flask import Blueprint, request, jsonify
from amadeus import Client, ResponseError
import os
import logging

bp = Blueprint('flight', __name__)

amadeus = Client(
    client_id=os.getenv('AMADEUS_KEY'),
    client_secret=os.getenv('AMADEUS_SECRET')
)

@bp.route('/api/flight/status', methods=['GET'])
def flight_status():
    carrier = request.args.get('carrier')
    number = request.args.get('number')
    date = request.args.get('date')

    if not all([carrier, number, date]):
        return jsonify({'error': 'Missing required parameters'}), 400

    try:
        response = amadeus.schedule.flights.get(
            carrierCode=carrier,
            flightNumber=number,
            scheduledDepartureDate=date
        )
        logging.info(f"Flight status for {carrier} {number} on {date}: {response.data}")
        return jsonify(response.data)
    except ResponseError as error:
        logging.error(f"Amadeus API error: {error}")
        return jsonify({'error': str(error)}), 500
