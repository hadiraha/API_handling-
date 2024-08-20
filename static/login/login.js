document.addEventListener('DOMContentLoaded', function(){
    const form = document.getElementById('loginForm');
    form.addEventListener('submit', async function(event) {
        event.preventDefault();

        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        try{
            const response = await fetch('/token', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `username=${username}&password=${password}`
            });

            if(!response.ok){
                throw new Error(`Error ocured!!!`);
            }
            const data = await response.json();
            if (data.access_token) {
                localStorage.setItem('token', data.access_token);
                window.location.href = '/static/index.html';
            } else {
                alert('Login faild');
            }
        } catch(error) {
            console.error("Failed to register:", error);
            document.getElementById('message').textContent = "Registration failed.";
        }
        
    });
});