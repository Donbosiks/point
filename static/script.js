function fetchClasses() {
    var grupas = document.getElementById('toggleSwitch').checked;
    fetch('/getClasses', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ group: grupas })
    })
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
    const classExplanation = document.getElementById('classExplanation_main');
    fetch('/getClassDetails', { method: 'POST', headers: 
        { 'Content-Type': 'application/json' }, 
        body: JSON.stringify({ class: classSelect }) }) 
        .then(response => response.json()) 
        .then(data => { // Отображение общего количества очков 
            classDetails.innerHTML = ` Punktu skaits: ${data.total_points}<br> `; // Отображение последних трех добавлений 
            classExplanation.innerHTML = data.details.map(cls => ` <div class="classExplanation_div"> <p>${cls.explanation}</p><p class="two">${cls.points_added}</p> </div> `).join(''); // Показать блок с деталями 
            details.style.display = 'block'; // Применение стилей к новым элементам 
            setTimeout(() => { document.querySelectorAll('.classExplanation_div').forEach(div => { div.classList.add('enlarged');

            });
            }, 0);
            }) .catch(error => { console.error('Error:', error);
            
        });
}


function updateTopClasses() {
    var grupas = document.getElementById('toggleSwitch').checked;
    fetch('/getTopClasses', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ group: grupas })
    })
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

document.getElementById('toggleSwitch').addEventListener('change', fetchClasses(), updateTopClasses())

// Обновление каждые 60 секунд
setInterval(updateTopClasses, 60000);
updateTopClasses();
fetchClasses();
