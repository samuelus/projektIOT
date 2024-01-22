/*
  Oczekiwany format odpowiedzi JSON dla endpointu /api/average-work-time:
  [
    {
      "id": "ddzp81l38vj1",
      "imie": "Monika",
      "nazwisko": "Nowicka",
      "sredni_czas": "3600"
    },
    {
      "id": "xd881l38hs1",
      "imie": "Jerzy",
      "nazwisko": "Sas",
      "sredni_czas": "5400"
    }
  ]
*/
function fetchAverageWorkTimeReport() {
    const startDate = document.getElementById('start-date').value;
    const endDate = document.getElementById('end-date').value;

    return fetch(`/api/average-work-time?start_date=${encodeURIComponent(startDate)}&end_date=${encodeURIComponent(endDate)}`, {
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

/*
  Oczekiwany format odpowiedzi JSON dla endpointu /api/total-work-time:
  [
    {
      "id": "ddzp81l38vj1",
      "imie": "Monika",
      "nazwisko": "Nowicka",
      "calkowity_czas": "3600"
    },
    {
      "id": "xd881l38hs1",
      "imie": "Jerzy",
      "nazwisko": "Sas",
      "calkowity_czas": "5400"
    }
  ]
*/

function fetchTotalWorkTimeReport() {
    const startDate = document.getElementById('start-date').value;
    const endDate = document.getElementById('end-date').value;

    return fetch(`/api/total-work-time?start_date=${encodeURIComponent(startDate)}&end_date=${encodeURIComponent(endDate)}`, {
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

/*
  Oczekiwany format odpowiedzi JSON dla endpointu /api/total-work-units:
  [
    {
      "id": "ddzp81l38vj1",
      "imie": "Monika",
      "nazwisko": "Nowicka",
      "naklad_pracy": "3"
    },
    {
      "id": "xd881l38hs1",
      "imie": "Jerzy",
      "nazwisko": "Sas",
      "naklad_pracy": "5"
    }
  ]
*/

function fetchTotalWorkUnitsReport() {
    const startDate = document.getElementById('start-date').value;
    const endDate = document.getElementById('end-date').value;

    return fetch(`/api/total-work-units?start_date=${encodeURIComponent(startDate)}&end_date=${encodeURIComponent(endDate)}`, {
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

function updateTableWithData(data, reportType) {
    const tableBody = document.getElementById('report-table-body');
    tableBody.innerHTML = '';

    data.forEach(employeeReportData => {
        const row = document.createElement('tr');
        let reportDataColumn = '';
        if (reportType === 'average') {
            reportDataColumn = `<td>${employeeReportData.sredni_czas}</td><td></td><td></td>`;
        } else if (reportType === 'total') {
            reportDataColumn = `<td></td><td>${employeeReportData.calkowity_czas}</td><td></td>`;
        } else if (reportType === 'units') {
            reportDataColumn = `<td></td><td></td><td>${employeeReportData.naklad_pracy}</td>`;
        }

        row.innerHTML = `
            <td>${employeeReportData.id}</td>
            <td>${employeeReportData.imie}</td>
            <td>${employeeReportData.nazwisko}</td>
            ${reportDataColumn}
        `;

        tableBody.appendChild(row);
    });
}


