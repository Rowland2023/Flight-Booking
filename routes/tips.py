from flask import Blueprint, request, jsonify
import logging

bp = Blueprint('tips', __name__)

@bp.route('/api/tips', methods=['GET'])
def get_travel_tips():
    city = request.args.get('city', '').strip().lower()

    TIPS = {
        "lagos": {
            "packing": "Light clothes, mosquito repellent, power bank.",
            "visa": "Visa required for most non-African countries.",
            "safety": "Avoid late-night travel, use trusted taxis.",
            "etiquette": "Greet elders respectfully, tipping is appreciated."
        },
        "london": {
            "packing": "Umbrella, layered clothing, travel adapter.",
            "visa": "Visa-free for many countries, check UK.gov.",
            "safety": "Very safe, watch for pickpockets in busy areas.",
            "etiquette": "Queue politely, avoid loud conversations."
        },
        "tokyo": {
            "packing": "Comfortable shoes, cash, phrasebook.",
            "visa": "Visa-free for many countries, check MOFA Japan.",
            "safety": "Extremely safe, follow local rules strictly.",
            "etiquette": "Bow when greeting, remove shoes indoors."
        }
    }

    tips = TIPS.get(city, {
        "packing": "Pack essentials based on weather.",
        "visa": "Check your country's embassy website.",
        "safety": "Research local safety guidelines.",
        "etiquette": "Respect local customs and culture."
    })

    logging.info(f"Travel tips for {city}: {tips}")
    return jsonify(tips)
