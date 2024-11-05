document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling for internal links
    const links = document.querySelectorAll('a[href^="#"]');
    for (const link of links) {
        link.addEventListener('click', function(event) {
            event.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            window.scrollTo({
                top: targetElement.offsetTop - 60, // Adjust for sticky header
                behavior: 'smooth'
            });
        });
    }

    // Interactive form validation
    const form = document.querySelector('form');
    const inputs = form.querySelectorAll('input, select, textarea');

    form.addEventListener('submit', function(event) {
        let formIsValid = true;

        inputs.forEach(input => {
            if (input.value.trim() === '' && input.hasAttribute('required')) {
                formIsValid = false;
                input.style.borderColor = 'red';
                input.nextElementSibling.textContent = 'This field is required';
                input.nextElementSibling.style.color = 'red';
            } else {
                input.style.borderColor = '#c0392b';
                if (input.nextElementSibling) {
                    input.nextElementSibling.textContent = '';
                }
            }
        });

        if (!formIsValid) {
            event.preventDefault();
        }
    });

    // Real-time input validation
    inputs.forEach(input => {
        input.addEventListener('input', () => {
            if (input.value.trim() === '' && input.hasAttribute('required')) {
                input.style.borderColor = 'red';
            } else {
                input.style.borderColor = '#c0392b';
            }
        });
    });
});
