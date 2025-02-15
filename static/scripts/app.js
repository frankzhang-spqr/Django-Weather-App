document.addEventListener('DOMContentLoaded', function() {
    const cityInput = document.getElementById('city');
    const cityDatalist = document.getElementById('city-suggestions');
    let timeoutId;

    cityInput.addEventListener('input', function() {
        clearTimeout(timeoutId);
        const query = this.value;

        if (query.length < 3) return;

        timeoutId = setTimeout(() => {
            fetch(`https://api.openweathermap.org/geo/1.0/direct?q=${query}&limit=5&appid=${API_KEY}`)
                .then(response => response.json())
                .then(data => {
                    cityDatalist.innerHTML = '';
                    data.forEach(city => {
                        const option = document.createElement('option');
                        const cityText = city.state ? 
                            `${city.name}, ${city.state}, ${city.country}` : 
                            `${city.name}, ${city.country}`;
                        option.value = city.name;
                        option.textContent = cityText;
                        cityDatalist.appendChild(option);
                    });
                })
                .catch(error => console.error('Error fetching cities:', error));
        }, 300);
    });

    // Location button functionality
    const locationBtn = document.getElementById('get-location');
    if (locationBtn) {
        locationBtn.addEventListener('click', function() {
            if (navigator.geolocation) {
                locationBtn.disabled = true;
                locationBtn.textContent = 'Getting location...';
                
                navigator.geolocation.getCurrentPosition(
                    function(position) {
                        const units = document.getElementById('units').value;
                        window.location.href = `/get-location-weather/?lat=${position.coords.latitude}&lon=${position.coords.longitude}&units=${units}`;
                    },
                    function(error) {
                        locationBtn.disabled = false;
                        locationBtn.textContent = '📍 Use My Location';
                        alert('Unable to get your location. Please check your browser settings.');
                        console.error('Geolocation error:', error);
                    }
                );
            } else {
                alert('Geolocation is not supported by your browser.');
            }
        });
    }

    // Favorite button functionality
    const favoriteBtn = document.querySelector('.favorite-btn');
    if (favoriteBtn) {
        favoriteBtn.addEventListener('click', function() {
            const city = this.dataset.city;
            
            fetch('/toggle-favorite/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({city: city})
            })
            .then(response => response.json())
            .then(data => {
                const starIcon = this.querySelector('i');
                const favoriteText = this.querySelector('.favorite-text');
                
                if (data.status === 'added') {
                    starIcon.classList.add('active');
                    favoriteText.textContent = 'Remove from Favorites';
                } else {
                    starIcon.classList.remove('active');
                    favoriteText.textContent = 'Add to Favorites';
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error updating favorites. Please try again.');
            });
        });
    }
});

// Function to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Set API key from Django template
const API_KEY = document.currentScript.getAttribute('data-api-key');
