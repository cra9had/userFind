const API_URL = "http://127.0.0.1:8000/api/"


document.addEventListener('DOMContentLoaded', async function () {
    const userData = await getUserInfo()
    if (!userData){
        document.location.href="/"
        return
    }
    document.getElementById("AuthMenu").style.display = "none"
    document.getElementById("userDropdown").innerText = userData["username"]
    document.getElementById("avatarImg").src = userData["avatar"]
    document.getElementById("user-photo").src = userData["avatar"]
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


document.getElementById("upload-photo").onchange = async function updateUserPhoto(event) {
    const userPhoto = document.getElementById('user-photo');
    const file = event.target.files[0];
    const token = localStorage.getItem("token")

    if (file) {
        const formData = new FormData();
        formData.append('avatar', file)
        await fetch(API_URL + 'auth/update/', {
            method: 'PATCH',
            headers: {
                "Authorization": "Token " + token
            },
            body: formData

        })
        location.reload()
    }
}

document.getElementById("saveSettings").onclick = async function () {
    const oldPassword = document.getElementById("old-password").value
    const newPassword = document.getElementById("new-password").value
    const token = localStorage.getItem("token")
    if (!(oldPassword && newPassword)) {
        return
    }

    const response = await fetch(API_URL + 'auth/change-password/', {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Token " + token
        },
        body: JSON.stringify({
            old_password: oldPassword,
            new_password: newPassword
        })
    })
    const fields = {
        "new_password": "new-password",
        "old_password": "old-password"
    }
    if (response.status === 200) {
        alert("Password changed successfully")
        location.reload()
    } else {
        const response_data = await response.json()
        console.log(response_data)
        Object.keys(response_data).forEach(errorField => {
            const error_message = response_data[errorField]
            addErrorToInput(document.getElementById(fields[errorField]), error_message)
        })
    }
}


function addErrorToInput(field, errorMessage) {
    field.placeholder = errorMessage;
    field.style.borderColor = 'red';
    field.value = ""
}
