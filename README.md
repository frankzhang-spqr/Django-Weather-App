# Weather Application

A modern, user-friendly weather application built with Django that provides real-time weather data and interactive maps.

## Features

### Core Features
- Real-time weather data display
- 5-day weather forecast
- Interactive map integration
- User location detection
- Temperature unit conversion (°C/°F)
- City search with auto-suggestions
- Mobile-responsive design

### User Features
- User authentication (register/login)
- Favorite cities management
- Personalized dashboard

### Technical Features
- OpenWeatherMap API integration
- OpenLayers map integration
- Responsive and accessible UI
- Progressive enhancement
- Cross-browser compatibility
- Optimized performance

## Technology Stack

### Backend
- **Python 3.x**: Core programming language
- **Django**: Web framework
- **SQLite**: Database (default)

### Frontend
- **HTML5/CSS3**: Structure and styling
- **JavaScript (ES6+)**: Client-side functionality
- **Font Awesome**: Icons
- **OpenLayers**: Interactive maps

### APIs
- OpenWeatherMap API: Weather data
- Geolocation API: User location detection

## Project Structure

```
Weather-App/
│
├── static/                # Static files
│   ├── scripts/           # JavaScript files
│   │   ├── app.js         # Main application logic
│   │   └── map.js         # Map functionality
│   │
│   └── styles/            # CSS files
│       ├── style.css      # Main styles
│       └── map.css        # Map-specific styles
│
├── templates/             # HTML templates
│   ├── index.html         # Homepage
│   ├── weather.html       # Weather details
│   ├── forecast.html      # 5-day forecast
│   ├── login.html         # User login
│   └── register.html      # User registration
│
├── weather_app/           # Main Django app
│   ├── views.py           # View controllers
│   ├── models.py          # Database models
│   ├── urls.py            # URL routing
│   ├── utils.py           # Utility functions
│   └── auth.py            # Authentication logic
│
└── weather_project/       # Django project settings
    ├── settings.py        # Project configuration
    └── urls.py            # Project URL routing
```

## Code Details

### Frontend Components

#### HTML Templates
- **base.html**: Base template with common elements
- **index.html**: Homepage with search and favorites
- **weather.html**: Current weather display with map
- **forecast.html**: 5-day forecast view
- **login.html/register.html**: Authentication forms

#### CSS Structure
- **style.css**: 
  - Modern, responsive design system
  - CSS variables for theming
  - Flexbox/Grid layouts
  - Smooth animations
  - Mobile-first approach
  - Accessibility features
  - Dark mode support

- **map.css**:
  - OpenLayers map customization
  - Custom controls styling
  - Responsive map layouts
  - Layer switcher design

#### JavaScript Modules
- **app.js**:
  - API integration
  - Search functionality
  - Location detection
  - Favorites management
  - Unit conversion
  - Dynamic updates

- **map.js**:
  - Map initialization
  - Layer management
  - Custom controls
  - Location markers
  - Weather overlays

### Backend Components

#### Models (models.py)
- User model extensions
- Favorite cities storage
- Search history tracking
- API cache management

#### Views (views.py)
- Weather data retrieval
- Forecast processing
- User authentication
- Favorites management
- API error handling

#### Utils (utils.py)
- API request handling
- Data formatting
- Cache management
- Error handling
- Location processing

## User Interface Features

### Visual Design
- Clean, modern aesthetic
- Intuitive navigation
- Responsive layouts
- Smooth transitions
- Clear typography
- Consistent spacing

### Interactive Elements
- Hoverable cards
- Animated buttons
- Loading states
- Error feedback
- Success messages
- Form validation

### Accessibility
- ARIA labels
- Keyboard navigation
- High contrast mode
- Reduced motion option
- Screen reader support
- Focus management

### Responsive Design
- Mobile-first approach
- Fluid layouts
- Adaptive components
- Touch-friendly controls
- Optimized images
- Performance focused

## Setting Up the Project

1. Clone the repository
```bash
git clone https://github.com/yourusername/Weather-App.git
cd Weather-App
```

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables
```bash
cp .env.example .env
# Edit .env with your OpenWeatherMap API key
```

5. Run migrations
```bash
python manage.py migrate
```

6. Start development server
```bash
python manage.py runserver
```

## API Configuration

1. Get an API key from [OpenWeatherMap](https://openweathermap.org/api)
2. Add the API key to your `.env` file:
```
OPENWEATHER_API_KEY=your_api_key_here
```

## Development Guidelines

### Code Style
- Follow PEP 8 for Python code
- Use ESLint for JavaScript
- Maintain consistent indentation
- Write clear comments
- Use meaningful variable names

### Best Practices
- Write unit tests
- Document code changes
- Use version control
- Handle errors gracefully
- Cache API responses
- Optimize database queries

## Browser Support

- Chrome (last 2 versions)
- Firefox (last 2 versions)
- Safari (last 2 versions)
- Edge (last 2 versions)
- Mobile browsers

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
