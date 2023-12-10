const API_URL = "http://127.0.0.1:8000/api/"

document.getElementById('search-type-select').addEventListener('change', function() {
    let firstContainer = document.getElementById('phone-search-form');
    let secondContainer = document.getElementById('fullname-birthday-search-form');

    firstContainer.classList.remove('active');
    secondContainer.classList.remove('active');

    if (this.value === '0') {
        firstContainer.classList.add('active');
    } else if (this.value === '1') {
        secondContainer.classList.add('active');
    }
});


document.addEventListener('DOMContentLoaded', async function () {
    // Variables to track the open state of popups
    let isLoginPopupOpen = false;
    let isRegisterPopupOpen = false;

    // Open login popup on button click
    const loginBtn = document.querySelector('.open-popup-btn[data-popup-id="loginPopup"]');
    const loginPopup = document.getElementById('loginPopup');
    const closeLoginBtn = document.getElementById('closeLoginBtn');

    loginBtn.addEventListener('click', function () {
        if (!isLoginPopupOpen && !isRegisterPopupOpen) {
            getCaptcha("LoginCaptchaContainer")
            loginPopup.style.display = 'block';
            isLoginPopupOpen = true;
        }
    });

    closeLoginBtn.addEventListener('click', function () {
        loginPopup.style.display = 'none';
        isLoginPopupOpen = false;
    });

    window.addEventListener('click', function (event) {
        if (event.target === loginPopup) {
            loginPopup.style.display = 'none';
            isLoginPopupOpen = false;
        }
    });

    // Open register popup on button click
    const registerBtn = document.querySelector('.open-popup-btn[data-popup-id="registerPopup"]');
    const registerPopup = document.getElementById('registerPopup');
    const closeRegisterBtn = document.getElementById('closeRegisterBtn');

    registerBtn.addEventListener('click', function () {
        if (!isLoginPopupOpen && !isRegisterPopupOpen) {
            getCaptcha("RegisterCaptchaContainer")
            registerPopup.style.display = 'block';
            isRegisterPopupOpen = true;
        }
    });

    closeRegisterBtn.addEventListener('click', function () {
        registerPopup.style.display = 'none';
        isRegisterPopupOpen = false;
    });

    window.addEventListener('click', function (event) {
        if (event.target === registerPopup) {
            registerPopup.style.display = 'none';
            isRegisterPopupOpen = false;
        }
    });

    const loginForm = document.getElementById('loginForm');
    loginForm.addEventListener('submit', async function (event) {
        event.preventDefault();
        const username = document.getElementById("loginUsername").value
        const password = document.getElementById("loginPassword").value
        const captcha_value = document.getElementById("LoginCaptchaContainer").querySelector('input[name="captchaCode"]').value
        const fields = {
            username: "loginUsername",
            password: "loginPassword",
            non_field_errors: "loginPassword",
            captcha_value: "LoginCaptchaContainer"
        }
        const response = await fetch(API_URL + "auth/login/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                username: username,
                password: password,
                captcha_key: sessionStorage.getItem("captcha_key"),
                captcha_value: captcha_value
            })
        })
        const response_data = await response.json()
        console.log(response_data)
        if (response.status === 400){
            Object.keys(response_data).forEach(errorField => {
                const error_message = response_data[errorField]
                addErrorToInput(document.getElementById(fields[errorField]), error_message)
            })
            sessionStorage.removeItem("captcha_key")
            getCaptcha("LoginCaptchaContainer")
        } else if (response.status === 200) {
            const token = response_data.token
            localStorage.setItem('token', token)
            sessionStorage.removeItem("captcha_key")
            location.reload()
        }
    });

    const registerForm = document.getElementById('registerForm');
    registerForm.addEventListener('submit', async function (event) {
        event.preventDefault();
        const username = document.getElementById("registerUsername").value
        const password = document.getElementById("registerPassword").value
        const password_confirm = document.getElementById("registerConfirmPassword").value
        const captcha_value = document.getElementById("RegisterCaptchaContainer").querySelector('input[name="captchaCode"]').value
        const fields = {
            username: "registerUsername",
            password: "registerPassword",
            password_confirm: "registerConfirmPassword",
            captcha_value: "LoginCaptchaContainer",
            non_field_errors: "registerConfirmPassword"
        }
        const response = await fetch(API_URL + "auth/register/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                username: username,
                password: password,
                password_confirm: password_confirm,
                captcha_key: sessionStorage.getItem("captcha_key"),
                captcha_value: captcha_value
            })
        })
        const response_data = await response.json()
        console.log(response_data)
        if (response.status === 400){
            Object.keys(response_data).forEach(errorField => {
                const error_message = response_data[errorField]
                addErrorToInput(document.getElementById(fields[errorField]), error_message)
            })
            sessionStorage.removeItem("captcha_key")
            getCaptcha("RegisterCaptchaContainer")
        } else if (response.status === 201) {
            const token = response_data.token
            localStorage.setItem('token', token)
            sessionStorage.removeItem("captcha_key")
            location.reload()
        }
    });
    const userData = await getUserInfo()
    if (!userData) {
        document.getElementById("userProfileMenu").style.display = "none"
    }  else {
        document.getElementById("AuthMenu").style.display = "none"
        document.getElementById("userDropdown").innerText = userData["username"]
        document.getElementById("avatarImg").src = userData["avatar"]
        document.getElementById("user-balance-amount").innerText = userData["balance"]
    }
    // setTimeout(function () {
    document.getElementById("loader").style.display = "none"
    document.getElementById("main-section").style.display = "block"
    document.getElementById("header-section").style.display = "flex"
    // }, 5000);
});


let intervalId


async function search(event) {
    async function getResult(pk){
        const response = await fetch(API_URL+"search/result/"+pk+"/", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Token " + localStorage.getItem("token")
            },
        })
        if (response.status === 204) {
            return
        } else if (response.status === 200) {
            const data = await response.json()
            if (data["status"] === 404 ){
                document.getElementById("main-section").style.display = "block"
                document.getElementById("searching-loader").style.display = "none"
                document.getElementById("userInfo").style.display = "none"
                document.getElementById("personNotFound").style.display = "inline-block"
                clearInterval(intervalId)
            }
            Object.keys(data).forEach(field => {
                if (field === "status"){
                    return
                }
                const infoElement = document.getElementById(field)
                infoElement.innerText = data[field]
                infoElement.parentNode.style.display = 'block'
            })
            document.getElementById("main-section").style.display = "block"
            document.getElementById("searching-loader").style.display = "none"
            document.getElementById("userInfo").style.display = "block"
            document.getElementById("personNotFound").style.display = "none"
            clearInterval(intervalId)
        }
    }

    event.preventDefault();
    const searchType = Number(document.getElementById("search-type-select").value)
    if (searchType === 0 ) {
        const phone = document.getElementById("phoneInput")
        if (!phone.value) {
            return addErrorToInput(phone, "Заполните это поле")
        }
        var searchQuery = {
            phone_number: phone.value.replace(/[^\d]/g, '')
        }
    } else if (searchType === 1) {
        const fullname = document.getElementById("fullnameInput")
        const birthday = document.getElementById("dateInput")
        if (!fullname.value) {
            return addErrorToInput(fullname, "Заполните это поле")
        }
        if (!birthday.value) {
            return addErrorToInput(birthday, "Заполните это поле")
        }
        var searchQuery = {
            fullname: fullname.value,
            birthday: birthday.value
        }
    } else {
        return
    }
    const fields = {
        "search_query": "phoneInput"
    }
    const response = await fetch(API_URL + "search/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Token " + localStorage.getItem("token")
        },
        body: JSON.stringify({
            search_type: searchType,
            search_query: searchQuery
        })
    })
    const data = await response.json()
    if (response.status === 201) {
        let pk = data["pk"]
        document.getElementById("main-section").style.display = "none"
        document.getElementById("searching-loader").style.display = "block"
        intervalId = setInterval(async function () {
            await getResult(pk)
        }, 1000);
    } else if (response.status === 400) {
        Object.keys(data).forEach(errorField => {
            const error_message = data[errorField]
            addErrorToInput(document.getElementById(fields[errorField]), error_message)
        })
    }

}


let elements = Array.from(document.querySelectorAll('.searchForm'));
elements.forEach(function(element) {
    element.addEventListener('submit', search)

})

function addErrorToInput(field, errorMessage) {
    field.placeholder = errorMessage
    field.style.borderColor = 'red'
    field.value = ""
}


async function getCaptcha(captcha_container){
    const current_time = new Date().getTime() / 1000
    if (sessionStorage.getItem("captcha_key") && Number(sessionStorage.getItem("captcha_expires")) > current_time){
        generateCaptcha(sessionStorage.getItem("captcha_image"), captcha_container)
        return
    }
    const response = await fetch(API_URL + "captcha/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
    })
    const data = await response.json()
    const expires = (new Date().getTime() / 1000) + 5 * 60
    sessionStorage.setItem('captcha_key', data["captcha_key"])
    sessionStorage.setItem('captcha_image', data["captcha_image"])
    sessionStorage.setItem('captcha_expires', expires.toString())
    generateCaptcha(data["captcha_image"], captcha_container)

}


function generateCaptcha(captcha_base64, captcha_container) {
    const captchaContainer = document.getElementById(captcha_container);

    const dummyCaptchaImageUrl = 'data:image/png;base64, ' + captcha_base64;
    const captchaImage = document.createElement('img');
    captchaImage.className = "auth-captcha-image"
    captchaImage.src = dummyCaptchaImageUrl;

    captchaContainer.innerHTML = '';
    captchaContainer.appendChild(captchaImage);

    const captchaInput = document.createElement('input');
    captchaInput.type = 'text';
    captchaInput.name = 'captchaCode';
    captchaInput.placeholder = 'Enter Captcha Code';

    captchaContainer.appendChild(captchaInput);
}


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


