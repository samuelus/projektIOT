import {showAlertForTime, logout} from './utils.js';

function fetchAverageWorkTimeReport() {
    if (!areDatesPresent()) {
        showAlertForTime('emptyDatesAlert', 3000);
        return;
    }
    if (!areDatesValid()) {
        showAlertForTime('invalidDatesAlert', 3000);
        return;
    }
    const startDate = document.getElementById('start-date').value;
    const endDate = document.getElementById('end-date').value;

    return fetch(`/api/odbicia/average-work-time?start_date=${encodeURIComponent(startDate)}&end_date=${encodeURIComponent(endDate)}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem('token')
        }
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            updateTableWithData(data, 'average');
        })
        .catch(error => console.error('Error fetching average work time:', error));
}

function fetchTotalWorkTimeReport() {
    if (!areDatesPresent()) {
        showAlertForTime('emptyDatesAlert', 3000);
        return;
    }
    if (!areDatesValid()) {
        showAlertForTime('invalidDatesAlert', 3000);
        return;
    }
    const startDate = document.getElementById('start-date').value;
    const endDate = document.getElementById('end-date').value;

    return fetch(`/api/odbicia/total-work-time?start_date=${encodeURIComponent(startDate)}&end_date=${encodeURIComponent(endDate)}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem('token')
        }
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            updateTableWithData(data, 'total');
        })
        .catch(error => console.error('Error fetching total work time:', error));
}

function fetchTotalWorkUnitsReport() {
    if (!areDatesPresent()) {
        showAlertForTime('emptyDatesAlert', 3000);
        return;
    }
    if (!areDatesValid()) {
        showAlertForTime('invalidDatesAlert', 3000);
        return;
    }
    const startDate = document.getElementById('start-date').value;
    const endDate = document.getElementById('end-date').value;

    return fetch(`/api/odbicia/total-work-unit?start_date=${encodeURIComponent(startDate)}&end_date=${encodeURIComponent(endDate)}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem('token')
        }
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            updateTableWithData(data, 'units');
        })
        .catch(error => console.error('Error fetching total work units:', error));
}

function fetchDataFromEmployeeEndpoint() {

    return fetch('api/pracownicy', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem('token')
        }
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .catch(error => console.error('Error:', error));
}

function formatDuration(durationInSeconds) {
    const hours = Math.floor(durationInSeconds / 3600);
    const minutes = Math.floor((durationInSeconds % 3600) / 60);
    const seconds = durationInSeconds % 60;

    return `${hours}h ${minutes}m ${seconds}s`;
}

function areDatesPresent() {
    const startDate = document.getElementById('start-date').value;
    const endDate = document.getElementById('end-date').value;
    return startDate && endDate;
}

function areDatesValid() {
    const startDate = document.getElementById('start-date').value;
    const endDate = document.getElementById('end-date').value;
    return startDate <= endDate;
}

function populateTableWithEmployeesData(employeesData) {
    const tableBody = document.getElementById('report-table-body');
    tableBody.innerHTML = '';

    employeesData.sort((a, b) => a.id.localeCompare(b.id));
    console.log(employeesData);

    employeesData.forEach(employeeData => {
        const row = document.createElement('tr');

        const idKartyCell = document.createElement('td');
        idKartyCell.textContent = employeeData.id;
        row.appendChild(idKartyCell);

        const imieCell = document.createElement('td');
        imieCell.textContent = employeeData.imie;
        row.appendChild(imieCell);

        const nazwiskoCell = document.createElement('td');
        nazwiskoCell.textContent = employeeData.nazwisko;
        row.appendChild(nazwiskoCell);

        tableBody.appendChild(row);
    });
}

function updateTableWithData(data, reportType)
{
    const tableBody = document.getElementById('report-table-body');
    const theadElement = document.getElementById('report-table').querySelector('thead tr');
    tableBody.innerHTML = '';
    theadElement.innerHTML = '';

    ['ID KARTY', 'IMIĘ', 'NAZWISKO'].forEach(headerText => {
        const header = document.createElement('th');
        header.textContent = headerText;
        theadElement.appendChild(header);
    });

    const specificHeaders = {
        'average': 'Średni Czas Pracy',
        'total': 'Całkowity Czas Pracy',
        'units': 'Zarejestrowane Wizyty'
    };

    const reportHeader = document.createElement('th');
    reportHeader.textContent = specificHeaders[reportType];
    theadElement.appendChild(reportHeader);

    // Now populate the body with data
    data.forEach(employeeReportData => {
        const row = document.createElement('tr');

        const idKartyCell = document.createElement('td');
        idKartyCell.textContent = employeeReportData.id_karty;
        row.appendChild(idKartyCell);

        const imieCell = document.createElement('td');
        imieCell.textContent = employeeReportData.imie;
        row.appendChild(imieCell);

        const nazwiskoCell = document.createElement('td');
        nazwiskoCell.textContent = employeeReportData.nazwisko;
        row.appendChild(nazwiskoCell);

        // Specific data cell based on report type
        const reportDataCell = document.createElement('td');
        if (reportType === 'average') {
            reportDataCell.textContent = formatDuration(employeeReportData.sredni_czas_pracy);
        } else if (reportType === 'total') {
            reportDataCell.textContent = formatDuration(employeeReportData.calkowity_czas_pracy);
        } else if (reportType === 'units') {
            reportDataCell.textContent = employeeReportData.zarejestrowane_wizyty;
        }
        row.appendChild(reportDataCell);

        tableBody.appendChild(row);
    });
}


document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('average-work-time-btn').addEventListener('click', fetchAverageWorkTimeReport);
    document.getElementById('total-work-time-btn').addEventListener('click', fetchTotalWorkTimeReport);
    document.getElementById('total-work-units-btn').addEventListener('click', fetchTotalWorkUnitsReport);
    document.getElementById('log-out-btn').addEventListener('click', logout);
});

document.addEventListener('DOMContentLoaded', function () {
    fetchDataFromEmployeeEndpoint().then(data => populateTableWithEmployeesData(data));
});

document.addEventListener('DOMContentLoaded', (event) => {
    if (!localStorage.getItem('token')) {
        window.location.href = '/loginPrompt.html';
    }
});

window.addEventListener('pageshow', function (event) {
    if (event.persisted) {
        window.location.reload();
    }
});


