function fetchDataFromImprintEndpoint() {
    return fetch('http://127.0.0.1:8080/api/odbicia', {
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

function populateImprintsTable(data) {
    const tableBody = document.getElementById('data-table-imprints');
    tableBody.innerHTML = '';

    data.forEach(item => {
        const row = document.createElement('tr');

        const idKartyCell = document.createElement('td');
        idKartyCell.textContent = item.id_karty;
        row.appendChild(idKartyCell);

        const idStrefyCell = document.createElement('td');
        idStrefyCell.textContent = item.id_strefy;
        row.appendChild(idStrefyCell);

        const czasWejsciaCell = document.createElement('td');
        czasWejsciaCell.textContent = item.czas_wejscia;
        row.appendChild(czasWejsciaCell);

        const czasWyjsciaCell = document.createElement('td');
        czasWyjsciaCell.textContent = item.czas_wyjscia ? item.czas_wyjscia : "Working...";
        row.appendChild(czasWyjsciaCell);

        tableBody.appendChild(row);
    });
}


document.addEventListener('DOMContentLoaded', function () {
    fetchDataFromImprintEndpoint().then(data => populateImprintsTable(data));
});
