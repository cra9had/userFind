var api_url = 'https://unmasking.net/api/';

// Check if the environment is local (you can adjust this condition based on your setup)
if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    // Override API URL for local development
    api_url = 'http://localhost:8000/api/';  // Change this to your local server URL
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


function openTopUpPopup() {
    const popup = document.getElementById("topUpPopup")
    popup.style.display = "block"
    window.addEventListener('click', function (event) {
        if (event.target === popup) {
            popup.style.display = 'none';
        }
    });
    document.getElementById("closeTopUp").onclick = function () {
        popup.style.display = "none"
    }
}


document.getElementById("TopUpButton").onclick = async function () {
    const amount = document.getElementById("topUpAmount")
    const token = localStorage.getItem("token")
    const searchType = Number(document.getElementById("topUpMethod").value)
    if (!amount.value){
        amount.placeholder = "Заполните поле!"
        amount.style.borderColor = 'red'
        return
    }
    const response = await fetch(api_url + "top-up/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Token " + token
        },
        body: JSON.stringify({
            amount: Number(amount.value),
            top_up_method: searchType
        })
    })
    const data = await response.json()
    if (response.status === 200){
        if (data.link) {
            window.location.href = data.link
        }
    } else {
        console.log(data)
        if (data.amount) {
            amount.value = ""
            amount.placeholder = data.amount
            amount.style.borderColor = 'red'
            return
        }
    }
}
