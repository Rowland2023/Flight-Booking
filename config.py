import os

# 🌤️ Weather API
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

# 📡 Flight Status API (placeholder for future integration)
FLIGHT_API_KEY = os.getenv('FLIGHT_API_KEY')
FLIGHT_STATUS_URL = "https://api.flightstatus.com/v1/status"  # Replace with real provider

# 🛫 Booking API (if you connect to real airline systems later)
BOOKING_API_KEY = os.getenv('BOOKING_API_KEY')
BOOKING_URL = "https://api.airline.com/v1/book"  # Replace with real provider

# 🗄️ Database Credentials
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'travelapp')
DB_USER = os.getenv('DB_USER', 'admin')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
