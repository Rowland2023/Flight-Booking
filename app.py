from flask import Flask
from flask_cors import CORS
import logging
import os
from dotenv import load_dotenv

# ✅ Load environment variables from .env file
load_dotenv()

# ✅ Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# ✅ Basic health check route
@app.route('/')
def home():
    return '✅ Flight Booking API is running.'

# ✅ Logging setup
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    filename='logs/flask.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

# ✅ Securely access API keys from environment
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
AMADEUS_CLIENT_ID = os.getenv('AMADEUS_CLIENT_ID')
AMADEUS_CLIENT_SECRET = os.getenv('AMADEUS_CLIENT_SECRET')

# ✅ Make keys available to route modules if needed
app.config['OPENWEATHER_API_KEY'] = OPENWEATHER_API_KEY
app.config['AMADEUS_CLIENT_ID'] = AMADEUS_CLIENT_ID
app.config['AMADEUS_CLIENT_SECRET'] = AMADEUS_CLIENT_SECRET

# ✅ Import and register route blueprints
from routes import weather, booking, airport, tips, status, flight

# Remove url_prefix='/api' from ALL registrations
app.register_blueprint(weather.bp)
app.register_blueprint(booking.bp)
app.register_blueprint(airport.bp) # FIXED
app.register_blueprint(tips.bp)    # FIXED
app.register_blueprint(status.bp)
app.register_blueprint(flight.bp)

# /weather, /booking, /airport, /tips, etc.

# ✅ Run the app
if __name__ == '__main__':
    port = int(os.environ.get('FLASK_PORT', 5000))
    app.run(host='0.0.0.0', port=port)
