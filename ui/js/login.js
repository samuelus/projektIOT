
function handleLoginFormSubmission(event) {
    event.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    performLogin({ username, password });
}

function performLogin(loginData) {
    fetch('api/admin/login', {
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
    window.location.href = 'imprints.html';
}

function handleLoginError(error) {
    console.error('Error logging in:', error);
    const alertElement = document.getElementById('loginFailAlert');
    alertElement.style.display = 'block';
    setTimeout(() => {
        alertElement.style.display = 'none';
    }, 3000);
}

document.getElementById('loginForm').addEventListener('submit', handleLoginFormSubmission);
