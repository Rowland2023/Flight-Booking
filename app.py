from flask import Flask
from flask_cors import CORS
import logging
import os
from dotenv import load_dotenv
load_dotenv()


from routes import weather, booking, airport, tips, status , flight

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Logging setup
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    filename='logs/flask.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

# Register Blueprints
app.register_blueprint(weather.bp)
app.register_blueprint(booking.bp)
app.register_blueprint(airport.bp)
app.register_blueprint(tips.bp)
app.register_blueprint(status.bp)
app.register_blueprint(flight.bp)

if __name__ == '__main__':
    port = int(os.environ.get('FLASK_PORT', 5000))
    app.run(host='0.0.0.0', port=port)


