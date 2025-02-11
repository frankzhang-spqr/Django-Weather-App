# Weather Dashboard

A modern and responsive Flask web application that provides real-time weather information and forecasts. Built with Python Flask and the OpenWeather API.

**Note**: Still devloping all the features below and adding new ones the plan is to be done by the end of March 

## Features

- 🌍 **Real-time Weather Data**: Get current weather conditions for any city worldwide
- 📍 **Geolocation Support**: Automatically fetch weather for your current location
- 🔍 **Smart Search**: City search with autocomplete suggestions
- 🌡️ **Unit Conversion**: Toggle between Fahrenheit and Celsius
- 📅 **5-Day Forecast**: View detailed weather forecasts
- 👤 **User Authentication**: Secure login and registration system
- ⭐ **Favorite Cities**: Save and manage your favorite locations
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

4. Create a `.env` file in the root directory and add your environment variables:
   ```
   API_KEY=your_openweather_api_key
   SECRET_KEY=your_secret_key
   FLASK_ENV=development
   ```
   Get your API key from [OpenWeather](https://openweathermap.org/api)

5. Run the application:
   ```bash
   python server.py
   ```

6. Open your browser and navigate to `http://localhost:8000`

## Deployment to Render.com

1. Create a new account on [Render](https://render.com) if you haven't already.

2. Create a new Web Service:
   - Connect your GitHub repository
   - Select the branch to deploy
   - Choose "Python 3" as the environment
   - Set the build command: `pip install -r requirements.txt`
   - Set the start command: `gunicorn server:app`

3. Add Environment Variables in Render Dashboard:
   - `API_KEY`: Your OpenWeather API key
   - `SECRET_KEY`: A secure random string for session management
   - `FLASK_ENV`: Set to "production"
   - `DATABASE_URL`: Will be automatically added by Render when you add PostgreSQL

4. Add PostgreSQL Database:
   - Go to "New +" in Render Dashboard
   - Select "PostgreSQL"
   - Connect it to your web service
   - The `DATABASE_URL` will be automatically added to your web service

5. Deploy your application.

## Features in Detail

### User Authentication
- Secure registration and login system
- Password encryption and validation
- Protected routes for authenticated users
- Flash messages for user feedback

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

### Favorite Cities
- Save frequently checked cities
- Quick access to favorite locations
- Easy management of saved cities

## Technologies Used

- **Backend**:
  - Python 3.x
  - Flask
  - Flask-Login for authentication
  - Flask-SQLAlchemy for database management
  - PostgreSQL for production database
  - SQLite for development
  - Gunicorn for production server

- **Frontend**:
  - HTML5
  - CSS3 with modern features (Grid, Flexbox, CSS Variables)
  - JavaScript (ES6+)
  - Font Awesome icons
  - OpenWeather API

## Database Schema

The application uses SQLAlchemy with the following model:

```python
class User:
    id: Integer (Primary Key)
    email: String (Unique)
    username: String (Unique)
    password_hash: String
    favorite_cities: JSON
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).
