document.addEventListener('DOMContentLoaded', function() {
    const stars = document.querySelectorAll('.star-rating label');

    stars.forEach(star => {
        star.addEventListener('click', function() {
            stars.forEach(s => s.classList.remove('selected'));
            this.classList.add('selected');
        });
    });
});