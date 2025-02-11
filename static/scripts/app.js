document.addEventListener('DOMContentLoaded', function() {
    // Check for geolocation support
    if ("geolocation" in navigator) {
        const locationButton = document.getElementById('get-location');
        locationButton.style.display = 'block';
        
        locationButton.addEventListener('click', function() {
            locationButton.disabled = true;
            locationButton.textContent = 'Getting location...';
            
            navigator.geolocation.getCurrentPosition(async function(position) {
                try {
                    const response = await fetch(`https://api.openweathermap.org/geo/1.0/reverse?lat=${position.coords.latitude}&lon=${position.coords.longitude}&limit=1&appid=${process.env.API_KEY}`);
                    const data = await response.json();
                    
                    if (data && data.length > 0) {
                        document.getElementById('city').value = data[0].name;
                        document.getElementById('weather-form').submit();
                    }
                } catch (error) {
                    console.error('Error getting location:', error);
                    alert('Unable to get your location. Please enter a city manually.');
                } finally {
                    locationButton.disabled = false;
                    locationButton.textContent = '📍 Use My Location';
                }
            }, function(error) {
                console.error('Geolocation error:', error);
                alert('Unable to get your location. Please enter a city manually.');
                locationButton.disabled = false;
                locationButton.textContent = '📍 Use My Location';
            });
        });
    }

    // Form validation and submission
    document.getElementById('weather-form').addEventListener('submit', function(event) {
        event.preventDefault();
       
        const city = document.getElementById('city').value;
        if (!city.trim()) {
            alert('Please enter a valid city name.');
            return;
        }

        // Show loading state
        document.getElementById('submit-btn').disabled = true;
        document.getElementById('submit-btn').textContent = 'Getting weather...';
        document.body.style.cursor = 'wait';
        
        // Proceed with form submission
        this.submit();
    });

    // Units toggle functionality
    document.getElementById('units').addEventListener('change', function() {
        if (document.getElementById('city').value.trim()) {
            document.getElementById('weather-form').submit();
        }
    });

    // Search suggestions
    let timeoutId;
    document.getElementById('city').addEventListener('input', function(e) {
        clearTimeout(timeoutId);
        const searchTerm = e.target.value.trim();
        
        if (searchTerm.length >= 3) {
            timeoutId = setTimeout(async () => {
                try {
                    const response = await fetch(`https://api.openweathermap.org/geo/1.0/direct?q=${searchTerm}&limit=5&appid=${process.env.API_KEY}`);
                    const cities = await response.json();
                    
                    const datalist = document.getElementById('city-suggestions');
                    datalist.innerHTML = '';
                    
                    cities.forEach(city => {
                        const option = document.createElement('option');
                        option.value = city.state ? 
                            `${city.name}, ${city.state}, ${city.country}` : 
                            `${city.name}, ${city.country}`;
                        datalist.appendChild(option);
                    });
                } catch (error) {
                    console.error('Error fetching city suggestions:', error);
                }
            }, 300);
        }
    });
});
