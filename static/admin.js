function fetchClasses() {
    fetch('/getClasses')
    .then(response => response.json())
    .then(classes => {
        const existingClassSelect = document.getElementById('existingClassSelect');
        existingClassSelect.innerHTML = classes.map(cls => `<option value="${cls.name}">${cls.name}</option>`).join('');
    });
}

function fetchCriteria() { 
    fetch('/getCriteria') 
    .then(response => response.json()) 
    .then(classes => { const classSelect = document.getElementById('criteriaSelect'); 
        classes.forEach(cls => { const newOption = document.createElement('option'); 
            newOption.value = cls.criteria_admin; 
            newOption.text = cls.criteria_admin; 
            classSelect.insertBefore(newOption, 
            classSelect.firstChild); 
        });
     });
     }

function check_value() {
    if(document.getElementById('criteriaSelect').value == "cits"){
        document.getElementById("classExplanation").style.display = "block"
    } else {
        document.getElementById("classExplanation").style.display = "none"
    }
}

document.addEventListener('DOMContentLoaded', fetchCriteria);

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
    const classExplanation = document.getElementById('criteriaSelect').value;

    if(document.getElementById('criteriaSelect').value == "cits"){
        const classExplanation = document.getElementById('classExplanation').value;
    }
    

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

function addCriteria() {
    const criteriaUser = document.getElementById('criteriaUser').value;
    const criteriaAdmin = document.getElementById('criteriaAdmin').value;

    console.log(criteriaUser)

    fetch('/addCriteria', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({criteriaUser: criteriaUser, criteriaAdmin: criteriaAdmin })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    });
}

fetchClasses();
