import {showAlertForTime} from "./utils.js";
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

function populateZoneSelect(zonesData, elementId) {
    const zoneSelect = document.getElementById(elementId);
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
        .then(data => populateZoneSelect(data, 'zoneSelect'))
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

function getEmployeeDetails(employeeId) {
    return fetch(`/api/pracownik/${employeeId}`, {
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
        .catch(error => {
            console.error('Error fetching employee details:', error);
        });
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

function editEmployee(employeeId, updatedData) {
    fetch(`api/pracownik/${employeeId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem('token')
        },
        body: JSON.stringify(updatedData)
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Success:', data);
            $('#editEmployeeModal').modal('hide');
            fetchDataFromEmployeeEndpoint().then(populateEmployeesTable);
        })
        .catch(error => {
            console.error('Error editing employee:', error);
        });
}

function populateEmployeesTable(data) {
    console.log(data);
    const tableBody = document.getElementById('data-table-employees');
    tableBody.innerHTML = '';

    data.forEach(item => {
        const row = document.createElement('tr');

        const cardIdEmployeeCell = document.createElement('td');
        cardIdEmployeeCell.textContent = item.id;
        row.appendChild(cardIdEmployeeCell);

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

        const editButtonCell = document.createElement('td');
        const editButton = document.createElement('button');
        editButton.textContent = 'Edytuj';
        editButton.className = 'btn btn-success';
        editButton.setAttribute('data-id', item.id);
        editButton.setAttribute('data-name', item.imie);
        editButton.setAttribute('data-surname', item.nazwisko);
        editButton.onclick = function () {
            openEditModal(item.id, item.imie, item.nazwisko);
        };
        editButtonCell.appendChild(editButton);
        row.appendChild(editButtonCell);

        tableBody.appendChild(row);
    });
}

function initializeEmployeeEventListeners() {
    fetchDataFromEmployeeEndpoint().then(data => populateEmployeesTable(data));

    document.getElementById('addEmployeeButton').addEventListener('click', handleAddEmployee);
    document.getElementById('editEmployeeButton').addEventListener('click', handleEditEmployee);
}

function handleAddEmployee() {
    const cardId = document.getElementById('cardId').value;
    const name = document.getElementById('name').value;
    const surname = document.getElementById('surname').value;
    const selectedZones = Array.from(document.getElementById('zoneSelect').options)
        .filter(option => option.selected)
        .map(option => parseInt(option.value));

    if (!cardId || !name || !surname || selectedZones.length === 0) {
        showAlertForTime('emptyDataAlertAdd', 4000);
        return;
    }
    if (doesCardIdExist(cardId)) {
        showAlertForTime('duplicateCardIdAlertAdd', 4000);
        return;
    }
    if (!isValidInput(name) || !isValidInput(surname)) {
        showAlertForTime('invalidDataAlertAdd', 4000);
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

function handleEditEmployee() {
    const initialCardId = document.getElementById('editEmployeeId').value;
    const name = document.getElementById('editEmployeeName').value;
    const surname = document.getElementById('editEmployeeSurname').value;
    const selectedZones = Array.from(document.getElementById('editEmployeeZoneSelect').options)
        .filter(option => option.selected)
        .map(option => parseInt(option.value));

    if (!name || !surname || selectedZones.length === 0) {
        showAlertForTime('emptyDataAlertEdit', 4000);
        return;
    }
    if (!isValidInput(name) || !isValidInput(surname)) {
        showAlertForTime('invalidDataAlertEdit', 4000);
        return;
    }

    const updatedData = {
        imie: name,
        nazwisko: surname,
        strefyDostepu: selectedZones
    };

    editEmployee(initialCardId, updatedData)
}

function openEditModal(employeeId, employeeName, employeeSurname) {
    Promise.all([fetchDataFromZoneEndpoint(), getEmployeeDetails(employeeId)])
        .then(([allZones, employeeDetails]) => {
            document.getElementById('editEmployeeId').value = employeeId;
            document.getElementById('editEmployeeName').value = employeeName;
            document.getElementById('editEmployeeSurname').value = employeeSurname;

            populateZoneSelect(allZones, 'editEmployeeZoneSelect');
            selectEmployeeZones(employeeDetails.strefyDostepu, 'editEmployeeZoneSelect');

            $('#editEmployeeModal').modal('show');
        })
        .catch(error => {
            console.error('Error in opening edit modal:', error);
        });
}

function selectEmployeeZones(employeeZones, elementId) {
    const zoneSelect = document.getElementById(elementId);

    console.log("Zones from select picker:", Array.from(zoneSelect.options));
    console.log("Zones from employee:", employeeZones);

    Array.from(zoneSelect.options).forEach(option => {
        const isZoneSelected = employeeZones.some(zone => {
            console.log(`Comparing option value (${option.value}) with zone id (${zone})`);
            return employeeZones.includes(Number(option.value));
        });

        console.log(`Option ${option.value} selected: ${isZoneSelected}`);
        option.selected = isZoneSelected;
    });


    $('.selectpicker').selectpicker('refresh');
}

function doesCardIdExist(cardId) {
    const cardIds = document.querySelectorAll('#data-table-employees td:nth-child(1)');
    for (let i = 0; i < cardIds.length; i++) {
        if (cardIds[i].textContent.trim() === cardId.trim()) {
            console.log("Card ID " + cardIds[i].textContent + " already exists.");
            return true;
        }
    }
    return false;
}


function isValidInput(input) {
    //letters uppercase and lowercase, numbers, spaces, apostrophes, and hyphens
    const regex = /^[A-Za-ząćęłńóśźżĄĆĘŁŃÓŚŹŻ '-]+$/;
    return regex.test(input);
}



document.addEventListener('DOMContentLoaded', initializeEmployeeEventListeners);

document.addEventListener('DOMContentLoaded', (event) => {
    if (!localStorage.getItem('token')) {
        window.location.href = '/loginPrompt.html';
    }
});