var API_URL = 'https://unmasking.net/api/';

// Check if the environment is local (you can adjust this condition based on your setup)
if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    // Override API URL for local development
    API_URL = 'http://localhost:8000/api/';  // Change this to your local server URL
}


document.addEventListener('DOMContentLoaded', async function () {
    const userData = await getUserInfo()
    if (!userData){
        document.location.href="/"
        return
    }
    document.getElementById("AuthMenu").style.display = "none"
    document.getElementById("userDropdown").innerText = userData["username"]
    document.getElementById("avatarImg").src = userData["avatar"]
    document.getElementById("user-balance-amount").innerText = userData["balance"]

    document.getElementById("loader").style.display = "none"
    document.getElementById("main-section").style.display = "block"
    document.getElementById("header-section").style.display = "flex"
})


async function getUserInfo(){
    const token = localStorage.getItem("token")
    if (!token) {
        return
    }
    const response = await fetch(API_URL + 'auth/user/', {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Token " + token
        },
    })
    if (response.status === 401) {
        localStorage.removeItem("token")
        return
    }
    return await response.json()
}
