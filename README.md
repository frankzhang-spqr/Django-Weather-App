# Weather Dashboard

A modern and responsive Flask web application that provides real-time weather information and forecasts. Built with Python Flask and the OpenWeather API.

## Features

- 🌍 **Real-time Weather Data**: Get current weather conditions for any city worldwide
- 📍 **Geolocation Support**: Automatically fetch weather for your current location
- 🔍 **Smart Search**: City search with autocomplete suggestions
- 🌡️ **Unit Conversion**: Toggle between Fahrenheit and Celsius
- 📅 **5-Day Forecast**: View detailed weather forecasts
- 📱 **Responsive Design**: Works seamlessly on desktop and mobile devices
- 🎨 **Modern UI**: Clean and intuitive interface with smooth animations

## Live Demo

Access the live application here: https://flask-weather-app-b3d4.onrender.com

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Flask-Weather-App.git
   cd Flask-Weather-App
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory and add your OpenWeather API key:
   ```
   API_KEY=your_api_key_here
   ```
   Get your API key from [OpenWeather](https://openweathermap.org/api)

5. Run the application:
   ```bash
   python server.py
   ```

6. Open your browser and navigate to `http://localhost:8000`

## Key Features Explained

### Geolocation
- Click the "Use My Location" button to automatically fetch weather for your current location
- Falls back to manual city search if geolocation is unavailable

### Weather Information
- Current temperature and "feels like" temperature
- Weather conditions with descriptive icons
- Wind speed and humidity levels
- Option to toggle between Fahrenheit and Celsius

### 5-Day Forecast
- Daily temperature ranges (high/low)
- Weather conditions and icons
- Wind speed and humidity forecasts
- Easy navigation between current weather and forecast views

### Search Functionality
- Real-time city suggestions as you type
- Support for international locations
- Clear error handling for invalid searches

## Technologies Used

- **Backend**:
  - Python 3.x
  - Flask
  - Requests library for API calls
  - python-dotenv for environment variables

- **Frontend**:
  - HTML5
  - CSS3 with modern features (Grid, Flexbox, CSS Variables)
  - JavaScript (ES6+)
  - Font Awesome icons
  - OpenWeather API

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).
