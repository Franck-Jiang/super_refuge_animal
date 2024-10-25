// script.js
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('signup-form');

    form.addEventListener('submit', (event) => {
        // Reset error messages
        resetErrors();

        // Validate the form
        let isValid = true;

        // Validate username
        const username = document.getElementById('username').value;
        if (username.length < 3) {
            showError('username-error', 'Username must be at least 3 characters long.');
            isValid = false;
        }

        // Validate email
        const email = document.getElementById('email').value;
        if (!validateEmail(email)) {
            showError('email-error', 'Please enter a valid email address.');
            isValid = false;
        }

        // Validate password
        const password = document.getElementById('password').value;
        if (password.length < 6) {
            showError('password-error', 'Password must be at least 6 characters long.');
            isValid = false;
        }

        // If the form is not valid, prevent submission
        if (!isValid) {
            event.preventDefault();
        }
    });

    function resetErrors() {
        document.querySelectorAll('.error-message').forEach((error) => {
            error.style.display = 'none';
        });
    }

    function showError(elementId, message) {
        const errorElement = document.getElementById(elementId);
        errorElement.textContent = message;
        errorElement.style.display = 'block';
    }

    function validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(String(email).toLowerCase());
    }
});
