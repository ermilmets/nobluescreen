document.addEventListener('DOMContentLoaded', function() {
    const stars = document.querySelectorAll('.star-rating label');

    stars.forEach(star => {
        star.addEventListener('click', function() {
            stars.forEach(s => s.classList.remove('selected'));
            this.classList.add('selected');
        });
    });
});

// document.addEventListener('DOMContentLoaded', function () {
//             var starRatingElement = document.querySelector('.star-rating-div');
//             var rating = parseFloat(starRatingElement.getAttribute('data-rating'));
//             var percentage = (rating / 5) * 100;
//             starRatingElement.style.setProperty('--rating-percentage', percentage + '%');
//         });
document.addEventListener('DOMContentLoaded', function () {
            var starRatings = document.querySelectorAll('.star-rating-div');
            starRatings.forEach(function (starRatingElement) {
                var rating = parseFloat(starRatingElement.getAttribute('data-rating'));
                var percentage = (rating / 5) * 100;
                starRatingElement.style.setProperty('--rating-percentage', percentage + '%');
            });
        });







