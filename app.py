from flask import Flask
from flask_cors import CORS
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import route modules
from routes import weather, booking, airport, tips, status, flight

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Logging setup
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    filename='logs/flask.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

# Register Blueprints with /api prefix
app.register_blueprint(weather.bp, url_prefix='/api')
app.register_blueprint(booking.bp, url_prefix='/api')
app.register_blueprint(airport.bp, url_prefix='/api')
app.register_blueprint(tips.bp, url_prefix='/api')
app.register_blueprint(status.bp, url_prefix='/api')
app.register_blueprint(flight.bp, url_prefix='/api')

# Run the app
if __name__ == '__main__':
    port = int(os.environ.get('FLASK_PORT', 5000))
    app.run(host='0.0.0.0', port=port)
