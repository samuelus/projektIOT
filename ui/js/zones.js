import {showAlertForTime } from "./utils.js";
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
        .catch(error => console.error('Error retrieving data:', error));
}

function addZone(zoneData) {
    fetch('api/strefa', {
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
    fetch(`api/strefa/${zoneId}`, {
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

function editZone(zoneId, newName) {
    fetch(`api/strefa/${zoneId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem('token')
        },
        body: JSON.stringify(newName)
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Success:', data);
            $('#editZoneModal').modal('hide');
            fetchDataFromZoneEndpoint().then(populateZonesTable);
        })
        .catch(error => {
            console.error('Error editing zone:', error);
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

        const editButtonCell = document.createElement('td');
        const editButton = document.createElement('button');
        editButton.textContent = 'Edytuj';
        editButton.className = 'btn btn-success';
        editButton.setAttribute('data-id', item.id);
        editButton.setAttribute('data-name', item.nazwaStrefy);
        editButton.onclick = function () {
            openEditModal(item.id, item.nazwaStrefy);
        };
        editButtonCell.appendChild(editButton);
        row.appendChild(editButtonCell);

        tableBody.appendChild(row);
    });
}

function openEditModal(id, name) {
    document.getElementById('editZoneId').value = id;
    document.getElementById('editZoneName').value = name;
    $('#editZoneModal').modal('show');
}

function initializeZoneEventListeners() {
    fetchDataFromZoneEndpoint().then(data => populateZonesTable(data));

    document.getElementById('addZoneButton').addEventListener('click', handleAddZoneClick);
    document.getElementById('editZoneButton').addEventListener('click', handleEditZoneClick);
}

function handleAddZoneClick() {
    const zoneName = document.getElementById('zoneName').value;
    console.log("Added zone Name:", zoneName);
    if (!zoneName) {
        showAlertForTime('emptyZoneNameAlertAdd', 4000);
        return;
    }
    if (doesZoneExist(zoneName)) {
        showAlertForTime('duplicateZoneNameAlertAdd', 4000);
        return;
    }
    if (!isValidInput(zoneName)) {
        showAlertForTime('invalidZoneNameAlertAdd', 4000);
        return;
    }
    addZone({nazwaStrefy: zoneName});
}

function handleEditZoneClick() {
    const zoneId = document.getElementById('editZoneId').value;
    const zoneName = document.getElementById('editZoneName').value;
    console.log("Edited zone Name:", zoneName);
    if (!zoneName) {
        showAlertForTime('emptyZoneNameAlertEdit', 4000);
        return;
    }
    if (doesZoneExist(zoneName)) {
        showAlertForTime('duplicateZoneNameAlertEdit', 4000);
        return;
    }
    if (!isValidInput(zoneName)) {
        showAlertForTime('invalidZoneNameAlertEdit', 4000);
        return;
    }
    editZone(zoneId, {nazwaStrefy: zoneName});
}

function doesZoneExist(zoneName) {
    const zones = document.querySelectorAll('#data-table-zones td:nth-child(2)');
    for (let i = 0; i < zones.length; i++) {
        if (zones[i].textContent.trim() === zoneName.trim()) {
            console.log("Zone " + zones[i].textContent + " already exists.");
            return true;
        }
    }
    return false;
}

function isValidInput(input) {
    //letters uppercase and lowercase, numbers, and spaces
    const regex = /^[A-Za-z0-9 ]+$/;
    return regex.test(input);
}

document.addEventListener('DOMContentLoaded', initializeZoneEventListeners);
document.addEventListener('DOMContentLoaded', (event) => {
    if (!localStorage.getItem('token')) {
        window.location.href = '/loginPrompt.html';
    }
});