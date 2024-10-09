# app.py (Flask Application)
from flask import Flask, render_template
import requests
from datetime import datetime
import pytz

app = Flask(__name__)

# Get your OpenWeather API key (store securely)
API_KEY = "7223fdda660a42b97338de79091c1f28"  # Replace with your OpenWeather API key
CITY = "Delhi, IN"  # Replace with your desired city
TIMEZONE = "Asia/Kolkata"  # Replace with your local timezone, e.g., "America/New_York"

def fetch_weather_data(city):
    """Fetch weather data from OpenWeather API."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def format_timestamp(unix_timestamp, timezone):
    """Convert Unix timestamp to local timezone."""
    local_tz = pytz.timezone(timezone)
    local_time = datetime.utcfromtimestamp(unix_timestamp).replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_time.strftime('%Y-%m-%d %H:%M:%S')

@app.route('/')
def home():
    """Render homepage with weather data."""
    weather_data = fetch_weather_data(CITY)
    if weather_data:
        # Convert the 'dt' field (Unix timestamp) to a readable local time
        weather_data['dt_formatted'] = format_timestamp(weather_data['dt'], TIMEZONE)
        return render_template('index.html', weather=weather_data)
    else:
        return "Failed to get weather data!"

if __name__ == "__main__":
    # Enable debug mode for auto-reloading
    app.run(debug=True)
