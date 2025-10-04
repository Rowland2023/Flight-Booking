import requests
from flask import Blueprint, request, jsonify, current_app

bp = Blueprint('tips', __name__)

def get_amadeus_token():
    url = 'https://test.api.amadeus.com/v1/security/oauth2/token'
    payload = {
        'grant_type': 'client_credentials',
        'client_id': current_app.config['AMADEUS_KEY'],
        'client_secret': current_app.config['AMADEUS_SECRET']
    }
    res = requests.post(url, data=payload)
    return res.json().get('access_token')

@bp.route('/tips', methods=['GET'])
def get_tips():
    city = request.args.get('city')
    token = get_amadeus_token()
    headers = { 'Authorization': f'Bearer {token}' }

    # Replace with actual Amadeus endpoint once available
    url = f'https://test.api.amadeus.com/v1/travel-recommendations?city={city}'
    res = requests.get(url, headers=headers)

    if res.status_code != 200:
        return jsonify({'error': 'No tips available'}), 404

    data = res.json()
    return jsonify({
        'packing': data.get('packingAdvice', 'No packing advice available.'),
        'visa': data.get('visaInfo', 'Visa info unavailable.'),
        'safety': data.get('safetyTips', 'No safety tips found.'),
        'etiquette': data.get('etiquette', 'Etiquette info not available.')
    })
