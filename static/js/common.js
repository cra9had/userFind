var API_URL = 'http://191.96.53.250/api/';

// Check if the environment is local (you can adjust this condition based on your setup)
if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    // Override API URL for local development
    API_URL = 'http://localhost:8000/api/';  // Change this to your local server URL
}



document.getElementById("logoutButton").onclick = async function () {
    const token = localStorage.getItem("token")
    localStorage.removeItem("token")
    await fetch(api_url + "auth/logout/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Token " + token
        }
    })
    location.reload()
}
