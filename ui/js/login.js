
function handleLoginFormSubmission(event) {
    event.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    performLogin({ username, password });
}

function performLogin(loginData) {
    fetch('http://127.0.0.1:8080/api/admin/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(loginData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Login failed');
        }
        return response.json();
    })
    .then(handleSuccessfulLogin)
    .catch(handleLoginError);
}

function handleSuccessfulLogin(data) {
    localStorage.setItem('token', data.token);
    window.location.href = 'zones.html';
}

function handleLoginError(error) {
    console.error('Error:', error);
    const errorMessageDiv = document.getElementById('error-message');
    errorMessageDiv.textContent = 'Nie udało się zalogować';
    errorMessageDiv.style.display = 'block';
}

document.getElementById('loginForm').addEventListener('submit', handleLoginFormSubmission);
