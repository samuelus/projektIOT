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

function populateZoneSelect(zonesData) {
    const zoneSelect = document.getElementById('zoneSelect');
    zoneSelect.innerHTML = '';

    zonesData.forEach(zone => {
        const option = document.createElement('option');
        option.value = zone.id;
        option.textContent = zone.nazwaStrefy;
        zoneSelect.appendChild(option);
    });

    $('.selectpicker').selectpicker('refresh');
}

$('#addEmployeeModal').on('show.bs.modal', function () {
    fetchDataFromZoneEndpoint()
        .then(data => populateZoneSelect(data))
        .catch(error => console.error('Error fetching zones:', error));
});

function fetchDataFromZoneEndpoint() {

    return fetch('api/strefy', {
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

function populateEmployeesTable(data) {
    console.log(data);
    const tableBody = document.getElementById('data-table-employees');
    tableBody.innerHTML = '';

    data.forEach(item => {
        const row = document.createElement('tr');

        const idEmployeeCell = document.createElement('td');
        idEmployeeCell.textContent = item.id;
        row.appendChild(idEmployeeCell);

        const nameEmployeeCell = document.createElement('td');
        nameEmployeeCell.textContent = item.imie;
        row.appendChild(nameEmployeeCell);

        const surnameEmployeeCell = document.createElement('td');
        surnameEmployeeCell.textContent = item.nazwisko;
        row.appendChild(surnameEmployeeCell);

        const deleteButtonCell = document.createElement('td');
        const deleteButton = document.createElement('button');
        deleteButton.textContent = 'Usuń';
        deleteButton.className = 'btn btn-danger';
        deleteButton.setAttribute('data-id', item.id);
        deleteButton.onclick = function () {
            deleteEmployee(item.id);
        };
        deleteButtonCell.appendChild(deleteButton);
        row.appendChild(deleteButtonCell);

        tableBody.appendChild(row);

        tableBody.appendChild(row);
    });
}

function initializeEmployeeEventListeners() {
    fetchDataFromEmployeeEndpoint().then(data => populateEmployeesTable(data));

    document.getElementById('addEmployeeButton').addEventListener('click', handleAddEmployeeClick);
}

function addEmployee(employeeData) {
    fetch('api/pracownik', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem('token')
        },
        body: JSON.stringify(employeeData)
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Success:', data);
            $('#addEmployeeModal').modal('hide');
            fetchDataFromEmployeeEndpoint().then(populateEmployeesTable);
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function deleteEmployee(employeeId) {
    fetch(`api/pracownik/${employeeId}`, {
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
            console.log(`Pracownik with ID ${employeeId} deleted successfully.`);
            return fetchDataFromEmployeeEndpoint();
        })
        .then(populateEmployeesTable)
        .catch(error => {
            console.error('Error deleting employee:', error);
        });
}

function handleAddEmployeeClick() {
    const cardId = document.getElementById('cardId').value;
    const name = document.getElementById('name').value;
    const surname = document.getElementById('surname').value;
    const selectedZones = Array.from(document.getElementById('zoneSelect').options)
        .filter(option => option.selected)
        .map(option => parseInt(option.value));

    if (!cardId || !name || !surname) {
        alert("Proszę wprowadzić wszystkie wymagane informacje.");
        return;
    }

    const employeeData = {
        id: cardId,
        imie: name,
        nazwisko: surname,
        strefyDostepu: selectedZones
    };

    addEmployee(employeeData)
}

document.addEventListener('DOMContentLoaded', initializeEmployeeEventListeners);