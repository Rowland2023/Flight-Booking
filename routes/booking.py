import requests
from flask import Blueprint, request, jsonify, current_app

bp = Blueprint('booking', __name__)

def get_amadeus_token():
    token_url = 'https://test.api.amadeus.com/v1/security/oauth2/token'
    payload = {
        'grant_type': 'client_credentials',
        'client_id': current_app.config['AMADEUS_KEY'],
        'client_secret': current_app.config['AMADEUS_SECRET']
    }
    res = requests.post(token_url, data=payload)
    return res.json().get('access_token')

@bp.route('/book-flight', methods=['POST'])
def book_flight():
    data = request.get_json()
    location = data.get('location')
    date = data.get('date')

    if not location or not date:
        return jsonify({'error': 'Missing destination or date'}), 400

    token = get_amadeus_token()
    headers = { 'Authorization': f'Bearer {token}' }

    # Simulate flight search from Lagos to destination
    search_url = 'https://test.api.amadeus.com/v2/shopping/flight-offers'
    params = {
        'originLocationCode': 'LOS',
        'destinationLocationCode': location.upper(),
        'departureDate': date,
        'adults': 1,
        'nonStop': False,
        'currencyCode': 'USD'
    }

    res = requests.get(search_url, headers=headers, params=params)
    if res.status_code != 200:
        return jsonify({'error': 'Flight search failed'}), 500

    offers = res.json().get('data', [])
    if not offers:
        return jsonify({'error': 'No flights found'}), 404

    # Return basic confirmation info
    first_offer = offers[0]
    itinerary = first_offer['itineraries'][0]['segments'][0]
    return jsonify({
        'confirmation': 'Booking Confirmed',
        'details': {
            'flight': itinerary['carrierCode'] + itinerary['number'],
            'departure': itinerary['departure']['iataCode'],
            'arrival': itinerary['arrival']['iataCode']
        }
    })
