function fetchDataFromZoneEndpoint() {

    return fetch('http://127.0.0.1:8080/api/strefy', {
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
        .catch(error => console.error('Error retrieving data:', error));
}

function addZone(zoneData) {
    fetch('http://127.0.0.1:8080/api/strefa', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem('token')
        },
        body: JSON.stringify(zoneData)
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Success:', data);
            $('#addZoneModal').modal('hide');
            fetchDataFromZoneEndpoint().then(populateZonesTable);
        })
        .catch(error => {
            console.error('Error adding zone:', error);
        });
}

function deleteZone(zoneId) {
    fetch(`http://127.0.0.1:8080/api/strefa/${zoneId}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem('token')
        }
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            console.log(`Zone with ID ${zoneId} deleted successfully.`);
            return fetchDataFromZoneEndpoint();
        })
        .then(populateZonesTable)
        .catch(error => {
            console.error('Error deleting zone:', error);
        });
}

function populateZonesTable(data) {
    //console.log(data);
    const tableBody = document.getElementById('data-table-zones');
    tableBody.innerHTML = '';

    data.forEach(item => {
        const row = document.createElement('tr');

        const idZoneCell = document.createElement('td');
        idZoneCell.textContent = item.id;
        row.appendChild(idZoneCell);

        const nameZoneCell = document.createElement('td');
        nameZoneCell.textContent = item.nazwaStrefy;
        row.appendChild(nameZoneCell);

        const deleteButtonCell = document.createElement('td');
        const deleteButton = document.createElement('button');
        deleteButton.textContent = 'Usuń';
        deleteButton.className = 'btn btn-danger';
        deleteButton.setAttribute('data-id', item.id);
        deleteButton.onclick = function () {
            deleteZone(item.id);
        };
        deleteButtonCell.appendChild(deleteButton);
        row.appendChild(deleteButtonCell);

        tableBody.appendChild(row);
    });
}

function initializeEventListeners() {
    fetchDataFromZoneEndpoint().then(data => populateZonesTable(data));

    document.getElementById('addZoneButton').addEventListener('click', handleAddZoneClick);
}

function handleAddZoneClick() {
    const zoneName = document.getElementById('zoneName').value;
    console.log("Zone Name:", zoneName);
    if (!zoneName) {
        alert("Proszę wprowadzić nazwę strefy.");
        return;
    }
    addZone({nazwaStrefy: zoneName});
}

document.addEventListener('DOMContentLoaded', initializeEventListeners);
