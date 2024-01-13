function fetchDataFromEndpoint() {
    return fetch('http://127.0.0.1:8080/api/strefy')
        .then(response => response.json())
        .catch(error => console.error('Error:', error));
}

function populateZonesTable(data) {
    const tableBody = document.getElementById('data-table-zones');
    tableBody.innerHTML = '';

    data.forEach(item => {
        const row = document.createElement('tr');

        const idStrefyCell = document.createElement('td');
        idStrefyCell.textContent = item.id;
        row.appendChild(idStrefyCell);

        const nameStrefyCell = document.createElement('td');
        nameStrefyCell.textContent = item.nazwaStrefy;
        row.appendChild(nameStrefyCell);

        tableBody.appendChild(row);
    });
}


document.addEventListener('DOMContentLoaded', function () {
    fetchDataFromEndpoint().then(data => populateZonesTable(data));
});
