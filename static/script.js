function fetchClasses() {
    fetch('/getClasses')
    .then(response => response.json())
    .then(classes => {
        const classSelect = document.getElementById('classSelect');
        classSelect.innerHTML = classes.map(cls => `<option value="${cls.name}">${cls.name}</option>`).join('');
    });
}

function showDetails() {
    const classSelect = document.getElementById('classSelect').value;
    const details = document.getElementById('details');
    const classDetails = document.getElementById('classDetails');

    fetch('/getClassDetails', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ class: classSelect })
    })
    .then(response => response.json())
    .then(data => {
        classDetails.innerHTML = `
            Punktu skaits: ${data.count}<br>
        `;
        details.style.display = 'block';
    });
}

function updateTopClasses() {
    fetch('/getTopClasses')
    .then(response => response.json())
    .then(data => {
        const topClassesDiv = document.getElementById('topClasses');
        topClassesDiv.innerHTML = data.map(cls => `
            <div>
                <h3 id="top_class_head">${cls.name}</h3>
                <p id="top_class_text">Punkti: ${cls.points}</p>
            </div>
        `).join('');
    });
}

// Обновление каждые 60 секунд
setInterval(updateTopClasses, 60000);
updateTopClasses();
fetchClasses();
