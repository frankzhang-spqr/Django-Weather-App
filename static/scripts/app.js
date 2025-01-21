document.getElementById('weather-form').addEventListener('submit', function(event) {
    event.preventDefault();
   
    const city = document.getElementById('city').value;
    if (!city.trim()) {
        alert('Please enter a valid city name.');
        return;
    }

    // Optionally add a loading spinner or some feedback to the user
    document.body.style.cursor = 'wait';
    this.submit();  // Proceed with the form submission after validation
});

