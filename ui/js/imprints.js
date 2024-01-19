function fetchDataFromImprintEndpoint() {
    return fetch('api/odbicia', {
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

function formatDateTime(dateTimeString) {
    const date = new Date(dateTimeString);

    const options = {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    };

    return date.toLocaleString('en-US', options);
}

function formatDuration(durationInSeconds) {
    const hours = Math.floor(durationInSeconds / 3600);
    const minutes = Math.floor((durationInSeconds % 3600) / 60);
    const seconds = durationInSeconds % 60;

    return `${hours}h ${minutes}m ${seconds}s`;
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
        czasWejsciaCell.textContent = formatDateTime(item.czas_wejscia);
        row.appendChild(czasWejsciaCell);

        const czasWyjsciaCell = document.createElement('td');
        czasWyjsciaCell.textContent = item.czas_wyjscia ? formatDateTime(item.czas_wyjscia) : "Working...";
        row.appendChild(czasWyjsciaCell);

        const czasPobytuCell = document.createElement('td');
        czasPobytuCell.textContent = item.czas_pobytu ? formatDuration(item.czas_pobytu) : "Working..." ;
        row.appendChild(czasPobytuCell);

        tableBody.appendChild(row);
    });
}


document.addEventListener('DOMContentLoaded', function () {
    fetchDataFromImprintEndpoint().then(data => populateImprintsTable(data));
});
