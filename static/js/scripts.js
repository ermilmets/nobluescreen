document.addEventListener('DOMContentLoaded', function() {
    const stars = document.querySelectorAll('.star-rating label');

    stars.forEach(star => {
        star.addEventListener('click', function() {
            stars.forEach(s => s.classList.remove('selected'));
            this.classList.add('selected');
        });
    });
});

document.addEventListener('DOMContentLoaded', function () {
            var starRatings = document.querySelectorAll('.star-rating-div');
            starRatings.forEach(function (starRatingElement) {
                var rating = parseFloat(starRatingElement.getAttribute('data-rating'));
                var percentage = (rating / 5) * 100;
                starRatingElement.style.setProperty('--rating-percentage', percentage + '%');
            });
        });


$(document).ready(function() {
            $('.add-to-cart-form').on('submit', function(event) {
                event.preventDefault();
                var form = $(this);
                var productId = form.data('product-id');
                var quantity = form.find('input[name="quantity"]').val();
                var csrfToken = form.find('input[name="csrfmiddlewaretoken"]').val();

                $.ajax({
                    url: '{% url "add_to_cart" 0 %}'.replace('0', productId),
                    type: 'POST',
                    data: {
                        'quantity': quantity,
                        'csrfmiddlewaretoken': csrfToken
                    },
                    success: function(response) {
                        $('#cart-alert').text('Product added to cart!').show().delay(3000).fadeOut();
                    },
                    error: function(response) {
                        $('#cart-alert').text('Failed to add product to cart.').show().delay(3000).fadeOut();
                    }
                });
            });
        });

document.addEventListener("DOMContentLoaded", function () {
        const apiKey = '5549b8bea1f894abb4e1ec8505cdf482';
        const city = 'Tallinn';
        const url = `https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${apiKey}&units=metric`;
        fetch(url)
            .then(response => response.json())
            .then(data => {
                const weatherWidget = document.getElementById('weather-widget');
                const temperature = data.main.temp;
                const description = data.weather[0].description;
                const icon = `http://openweathermap.org/img/wn/${data.weather[0].icon}.png`;
                weatherWidget.innerHTML = `<img src="${icon}" alt="${description}"> ${temperature}°C, ${description}, ${city}`;
            })
            .catch(error => {
                const weatherWidget = document.getElementById('weather-widget');
                weatherWidget.innerHTML = `Failed to load weather data`;
                console.error('Error fetching weather data:', error);
            });
    });

document.addEventListener("DOMContentLoaded", function () {
    const weatherWidget = document.getElementById('weather-widget');
    const dateTimeElement = document.getElementById('date-time');
    const apiKey = '5549b8bea1f894abb4e1ec8505cdf482';

    fetch('https://ipinfo.io/json?token=e1e7f551601cab')
        .then(response => response.json())
        .then(locationData => {
            const city = locationData.city;
            const region = locationData.region;
            const country = locationData.country;
            const weatherUrl = `https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${apiKey}&units=metric`;
            return fetch(weatherUrl).then(response => response.json()).then(weatherData => {
                const temperature = weatherData.main.temp;
                const description = weatherData.weather[0].description;
                const icon = `http://openweathermap.org/img/wn/${weatherData.weather[0].icon}.png`;
                weatherWidget.innerHTML = `
                    <img src="${icon}" alt="${description}">
                    ${temperature}°C, ${description}
                    <br>
                    ${city}, ${region}, ${country}
                `;
            });
        })
        .catch(error => {
            weatherWidget.innerHTML = 'Failed to load weather data';
            console.error('Error fetching location or weather data:', error);
        });

    function updateDateTime() {
        const now = new Date();
        const options = {
            weekday: 'long',
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            hourCycle: 'h23'
        };
        const dateTimeString = now.toLocaleDateString('en-US', options);
        dateTimeElement.textContent = dateTimeString;
    }

    setInterval(updateDateTime, 1000);
});

$('.carousel').carousel({
      interval: 1000 //
    });






