function fetchClasses() {
    fetch('/getClasses', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ group: null })
    })
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
            newOption.value = cls.criteria_user; 
            newOption.text = cls.criteria_user; 
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


fetchClasses();
