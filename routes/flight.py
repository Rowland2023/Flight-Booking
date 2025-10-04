from flask import Blueprint, request, jsonify, current_app
from amadeus import Client, ResponseError
import logging

bp = Blueprint('flight', __name__)

# Initialize Amadeus client using Flask config
def init_amadeus_client():
    return Client(
        client_id=current_app.config['AMADEUS_CLIENT_ID'],
        client_secret=current_app.config['AMADEUS_CLIENT_SECRET']
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
        amadeus = init_amadeus_client()
        response = amadeus.schedule.flights.get(
            carrierCode=carrier,
            flightNumber=number,
            scheduledDepartureDate=date
        )
        logging.info(f"✅ Flight status for {carrier} {number} on {date}: {response.data}")
        return jsonify(response.data)

    except ResponseError as error:
        logging.error(f"❌ Amadeus API error for {carrier} {number} on {date}: {error}")
        return jsonify({'error': 'Unable to retrieve flight status'}), 502
