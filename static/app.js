document.addEventListener('DOMContentLoaded', function() {
    let skip = 0;
    const limit = 10;

    fetchUsernames();

    document.getElementById('showMore').addEventListener('click', () => {
        skip += limit;
        fetchUsernames(skip, limit);
    });

    async function fetchUsernames(skip = 0, limit = 10){
        try{
            const response = await fetch(`/usernames?skip=${skip}&limit=${limit}`);
            if (!response.ok){
                throw new Error(`An error has taken place: ${response.statusText}`);
            }
            const usernames = await response.json();
            const list = document.getElementById('usernameList');
            // list.innerHTML = "";

            usernames.forEach(username => {
                const button = document.createElement('button');
                button.textContent = username;
                button.classList.add('username_button');
                button.addEventListener('click', () => fetchProfile(username));
                list.appendChild(button);
            });
        } catch (error){
            console.error("Failed to fetch from usernames:", error);
            const list = document.getElementById('usernameList');
            list.innerHTML = "<li>Error to catch from usernames<li>";
        }
    }

    
    async function fetchProfile(username){
        try {
            const response = await fetch(`/profiles/username/${username}`);
            if (!response.ok){
                throw new Error(`An error has taken place: ${response.statusText}`);
            }
            const profile = await response.json();
            const details = document.getElementById('profileDetail');
            details.innerHTML = `
                <p>Username: ${profile.username}</p>
                <p>Name: ${profile.name}</p>
                <p>Followers: ${profile.follower_cnt}</p>
                <p>Follower Count (Number): ${profile.follower_cnt_num}</p>
                <p>Follow: ${profile.follow_cnt}</p>
                <p>URL: ${profile.url}</p>
                <p>Video Counter: ${profile.video_cnt}</p>
                <p>Description: ${profile.description}</p>
            `;
        } catch (error) {
            console.error("Failed to fetch from profiles:", error);
            const details = document.getElementById('profileDetail');
            details.innerHTML = "<li>Error to catch from profiles<li>";
        }
    }
 
});