document.addEventListener('DOMContentLoaded', function() {
    // Geolocation support
    if ("geolocation" in navigator) {
        const locationButton = document.getElementById('get-location');
        locationButton.style.display = 'block';
        
        locationButton.addEventListener('click', function() {
            locationButton.disabled = true;
            locationButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Getting location...';
            
            navigator.geolocation.getCurrentPosition(
                async function(position) {
                    try {
                        const units = document.getElementById('units').value;
                        window.location.href = `/get_location_weather?lat=${position.coords.latitude}&lon=${position.coords.longitude}&units=${units}`;
                    } catch (error) {
                        console.error('Error getting location:', error);
                        alert('Unable to get your location. Please enter a city manually.');
                    } finally {
                        locationButton.disabled = false;
                        locationButton.innerHTML = '📍 Use My Location';
                    }
                },
                function(error) {
                    console.error('Geolocation error:', error);
                    let errorMsg = 'Unable to get your location. ';
                    switch (error.code) {
                        case error.PERMISSION_DENIED:
                            errorMsg += 'Please allow location access and try again.';
                            break;
                        case error.POSITION_UNAVAILABLE:
                            errorMsg += 'Location information is unavailable.';
                            break;
                        case error.TIMEOUT:
                            errorMsg += 'Location request timed out.';
                            break;
                        default:
                            errorMsg += 'Please enter a city manually.';
                    }
                    alert(errorMsg);
                    locationButton.disabled = false;
                    locationButton.innerHTML = '📍 Use My Location';
                },
                {
                    enableHighAccuracy: true,
                    timeout: 10000,
                    maximumAge: 0
                }
            );
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
        const submitBtn = document.getElementById('submit-btn');
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
        document.body.style.cursor = 'wait';
        
        // Proceed with form submission
        this.submit();
    });

    // Units toggle functionality
    document.getElementById('units').addEventListener('change', function() {
        const city = document.getElementById('city').value.trim();
        if (city) {
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
                    const response = await fetch(`/search?q=${searchTerm}`);
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

    // Favorite city functionality
    const favoriteBtn = document.getElementById('favorite-btn');
    if (favoriteBtn) {
        favoriteBtn.addEventListener('click', async function() {
            try {
                const city = this.dataset.city;
                const response = await fetch('/toggle_favorite', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ city }),
                });
                
                const data = await response.json();
                
                if (data.status === 'added') {
                    this.innerHTML = '<i class="fas fa-star"></i>';
                    this.classList.add('active');
                } else {
                    this.innerHTML = '<i class="far fa-star"></i>';
                    this.classList.remove('active');
                }
            } catch (error) {
                console.error('Error toggling favorite:', error);
                alert('Unable to update favorite cities. Please try again.');
            }
        });
    }

    // Flash messages auto-hide
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => message.remove(), 300);
        }, 5000);
    });
});
