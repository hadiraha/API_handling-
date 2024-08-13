document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('registerForm');
    form.addEventListener('submit', async function(event) {
        event.preventDefault();

        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        try{
            const response = await fetch('/users/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({username, password}),
            });

            if (!response.ok) {
                throw new Error(`Error occured: ${response.statusText}`);
            }

            document.getElementById('message').textContent = "You got registered!";
            document.getElementById('message').style.color = "green";

        } catch(error) {
            console.error("Failed to register:", error);
            document.getElementById('message').textContent = "Registration failed.";
        }
        
    });
});