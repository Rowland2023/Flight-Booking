import requests
from flask import Blueprint, request, jsonify, current_app
from requests.exceptions import RequestException
import json # Used for logging/debugging

# ⬅️ IMPORT the reusable functions from the airport module
from .airport import get_amadeus_token, lookup_airport_data 

bp = Blueprint('booking', __name__)

# Helper function to extract IATA code from the full airport lookup data
def extract_iata_code(city: str) -> str or None:
    """Uses the reusable airport data function to find the city's IATA code."""
    
    # 1. Call the robust core airport lookup function directly
    data, status = lookup_airport_data(city)

    if status == 200 and data.get('airports'):
        # Return the IATA code of the first airport found
        return data['airports'][0].get('iata')
    
    # Log the failure reason for debugging the 400 error
    current_app.logger.warning(f"⚠️ IATA lookup failed for '{city}'. Status: {status}. Response: {data.get('error', 'Unknown')}")
    return None

# ✅ Route updated for direct connection
@bp.route('/api/book-flight', methods=['POST'])
def book_flight():
    # Attempt to get JSON data silently
    data = request.get_json(silent=True)

    # --- Initial Validation: Check for JSON body and required fields ---
    if data is None:
        current_app.logger.error("❌ Booking received no JSON data. Check frontend Content-Type header.")
        return jsonify({"error": "Request body missing or invalid JSON"}), 400

    location = data.get('location')
    date = data.get('date')
    
    # Log received data for debugging the 400 error
    current_app.logger.info(f"Received booking request: Location={location}, Date={date}")

    if not location or not date:
        return jsonify({'error': 'Missing destination or date'}), 400

    # --- IATA Lookup: Using the refactored internal call ---
    iata_code = extract_iata_code(location) 
    
    if not iata_code:
        # This is where the 400 error originates when city lookup fails
        return jsonify({'error': f'Could not resolve IATA code for {location}. Check spelling.'}), 400

    # --- Token and Flight Search ---
    token = get_amadeus_token()
    if not token:
        return jsonify({'error': 'Failed to retrieve Amadeus token'}), 502

    headers = { 'Authorization': f'Bearer {token}' }
    search_url = 'https://test.api.amadeus.com/v2/shopping/flight-offers'
    params = {
        # Using a fixed origin for now; can be made dynamic later
        'originLocationCode': 'LOS', 
        'destinationLocationCode': iata_code,
        'departureDate': date,
        'adults': 1,
        'nonStop': False,
        'currencyCode': 'USD'
    }

    try:
        res = requests.get(search_url, headers=headers, params=params)
        
        if res.status_code != 200:
            current_app.logger.error(f"❌ Flight search failed: {res.status_code} - {res.text}")
            # Return the external API's status code and error details
            details = res.json().get('errors', res.text)
            return jsonify({'error': 'Flight search failed', 'details': details}), res.status_code

        offers = res.json().get('data', [])
        if not offers:
            current_app.logger.warning(f"⚠️ No flights found to {location} on {date}")
            return jsonify({'message': f'No flights available to {location} on {date}'}), 200

        # --- Successful Flight Found (Mock Booking Confirmation) ---
        first_offer = offers[0]
        itinerary = first_offer['itineraries'][0]['segments'][0]

        current_app.logger.info(f"✅ Flight confirmed: {itinerary['carrierCode']}{itinerary['number']} to {itinerary['arrival']['iataCode']}")

        return jsonify({
            'confirmation': 'Booking Search Complete', # Changed from 'Confirmed' as this is only search
            'details': {
                'flight': itinerary['carrierCode'] + itinerary['number'],
                'departure': itinerary['departure']['iataCode'],
                'arrival': itinerary['arrival']['iataCode'],
                'price': first_offer['price']['total']
            }
        })
        
    except RequestException as e:
        current_app.logger.error(f"Network error during flight search: {e}")
        return jsonify({"error": "Failed to connect to Amadeus flight search."}), 503
    except Exception as e:
        current_app.logger.critical(f"Unhandled error in booking: {e}", exc_info=True)
        return jsonify({"error": "Internal server crash during flight search."}), 500