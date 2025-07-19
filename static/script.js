document.addEventListener('DOMContentLoaded', () => {
    const attendanceForm = document.getElementById('attendanceForm');
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    const submitBtn = document.getElementById('submitBtn');
    const loadingDiv = document.getElementById('loading');
    const resultsDiv = document.getElementById('results');
    const errorDiv = document.getElementById('error');
    const errorMessageElem = errorDiv.querySelector('.error-message');

    const messageElem = document.getElementById('message');
    const attendanceDetailsDiv = document.getElementById('attendanceDetails');
    const presentCountElem = document.getElementById('presentCount');
    const absentCountElem = document.getElementById('absentCount');
    const percentageElem = document.getElementById('percentage');

    attendanceForm.addEventListener('submit', async (event) => {
        event.preventDefault(); // Prevent default form submission

        // Hide previous messages
        resultsDiv.classList.add('hidden');
        errorDiv.classList.add('hidden');
        attendanceDetailsDiv.classList.add('hidden');
        errorMessageElem.textContent = '';
        messageElem.textContent = '';

        // Show loading spinner
        loadingDiv.classList.remove('hidden');
        submitBtn.disabled = true; // Disable button during submission

        const username = usernameInput.value;
        const password = passwordInput.value;

        try {
            const response = await fetch('/get_attendance', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password }),
            });

            const data = await response.json();

            if (data.success) {
                messageElem.textContent = data.message;
                if (data.present !== undefined && data.absent !== undefined) {
                    presentCountElem.textContent = data.present;
                    absentCountElem.textContent = data.absent;
                    percentageElem.textContent = data.percentage;
                    attendanceDetailsDiv.classList.remove('hidden');
                }
                resultsDiv.classList.remove('hidden');
            } else {
                errorMessageElem.textContent = data.message || "An unknown error occurred.";
                errorDiv.classList.remove('hidden');
            }
        } catch (error) {
            console.error('Fetch error:', error);
            errorMessageElem.textContent = "Could not connect to the server or an unexpected error occurred. Please try again later.";
            errorDiv.classList.remove('hidden');
        } finally {
            loadingDiv.classList.add('hidden'); // Hide loading spinner
            submitBtn.disabled = false; // Re-enable button
        }
    });
});