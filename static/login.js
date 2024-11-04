function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    fetch('/login_check', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: username, password: password })
    })
    .then(response => response.json().then(data => {
        if (response.ok) {
            window.location.href = data.redirect;
        } else {
            document.getElementById('login_error').style.display = 'block';
        }
    }))
    .catch(error => {
        console.error('Error:', error);
    });

}