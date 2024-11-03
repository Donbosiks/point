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
    const classPoints = parseInt(document.getElementById('classPoints').value) || 0;
    const classExplanation = document.getElementById('classExplanation').value;

    fetch('/addClass', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: className, points: classPoints})
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

function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    fetch('/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: username, password: password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message === 'Login successful') {
            // Скрываем контейнер для входа и показываем админ-контейнер
            document.getElementById('login-container').style.display = 'none';
            document.getElementById('admin-container').style.display = 'block';
        } else {
            alert('Invalid credentials');
        }
    });
}

// При загрузке страницы всегда показываем контейнер для входа
window.onload = function() {
    document.getElementById('login-container').style.display = 'block';
    document.getElementById('admin-container').style.display = 'none';
}

// // Проверяем состояние входа при загрузке страницы
// window.onload = function() {
//     if (localStorage.getItem('loggedIn') === 'true') {
//         document.getElementById('login-container').style.display = 'none';
//         document.getElementById('admin-container').style.display = 'block';
//     }
// }
