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
    let classExplanation = document.getElementById('criteriaSelect').value;

    if(document.getElementById('criteriaSelect').value == "cits"){
        classExplanation = document.getElementById("classExplanation").value;
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

function uploadPDF() {
    const formData = new FormData();
    const pdfFile = document.getElementById('pdfFile').files[0];
    const pdfFile_1 = document.getElementById('pdfFile_1').files[0];

    // Проверка и добавление первого файла
    if (pdfFile) {
        formData.append('pdf', pdfFile);
    } else {
        formData.append('pdf', 'none');
    }

    // Проверка и добавление второго файла
    if (pdfFile_1) {
        formData.append('pdf_1', pdfFile_1);
    } else {
        formData.append('pdf_1', 'none');
    }

    fetch('/upload_criteria', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById('response').innerText = `Error: ${data.error}`;
        } else {
            document.getElementById('response').innerText = `Success: ${data.message}`;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('response').innerText = 'An error occurred while uploading the file.';
    });
}



fetchClasses();
