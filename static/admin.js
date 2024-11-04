function fetchClasses() {
    fetch('/getClasses')
    .then(response => response.json())
    .then(classes => {
        const existingClassSelect = document.getElementById('existingClassSelect');
        existingClassSelect.innerHTML = classes.map(cls => `<option value="${cls.name}">${cls.name}</option>`).join('');
    });
}

function addClass() {
    const className = document.getElementById('className').value;

    fetch('/addClass', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: className})
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        fetchClasses(); // Обновление списка классов
    });
}

function addPoints() {
    const className = document.getElementById('existingClassSelect').value;
    const classPoints = parseInt(document.getElementById('classPoints').value);
    const classExplanation = document.getElementById('classExplanation').value;

    fetch('/addPoints', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: className, points: classPoints, explanation: classExplanation })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    });
}

fetchClasses();
