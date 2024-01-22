function hideAllAlerts() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => alert.style.display = 'none');
}

function showAlertForTime(alertId, duration) {
    hideAllAlerts();
    const alertElement = document.getElementById(alertId);
    alertElement.style.display = 'block';
    setTimeout(() => {
        alertElement.style.display = 'none';
    }, duration);
}

function logout() {
    console.log('Logging out...');
    localStorage.removeItem('token');
    window.location.href = '/';
}

export {hideAllAlerts, showAlertForTime, logout};