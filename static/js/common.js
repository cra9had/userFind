const api_url = "http://127.0.0.1:8000/api/"


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
