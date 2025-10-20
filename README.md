# 🕵️‍♂️ Unmasking — User Data Lookup Platform

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)]()
[![Django](https://img.shields.io/badge/Django-4.x-green.svg)]()
[![DRF](https://img.shields.io/badge/DRF-REST-blue.svg)]()
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-DB-blue.svg)]()
[![Redis](https://img.shields.io/badge/Redis-Cache-red.svg)]()
[![Celery](https://img.shields.io/badge/Celery-Tasks-orange.svg)]()

**Unmasking** is a backend platform for retrieving and analyzing public user data at scale.  
It provides APIs for querying millions of users, with secure access, trial periods, and paid features.

---

## 🚀 Features

- 🔍 **User Search API** — Full or masked results depending on subscription/payment.  
- 🧾 **Personal Account** — Users can manage subscriptions, view history, and access trial period.  
- 🛡️ **Security** — Google Captcha integration and password recovery.  
- 💳 **Payments** — Support for card payments (Payok) and cryptocurrency (OXAPAY).  
- ⚡ **Asynchronous Tasks** — Background processing via Celery + Redis.  
- 🗄️ **Database** — PostgreSQL for robust storage and querying.

---

## 🧩 Tech Stack

| Component | Description                       |
|------------|-----------------------------------|
| **Backend** | Django, Django REST Framework     |
| **Async Tasks** | Celery + Redis                    |
| **Database** | PostgreSQL                        |
| **Authentication** | Google Captcha, Password Recovery |
| **Payments** | Payok (cards), OXAPAY (crypto)    |
| **DevOps** | Docker (Optional)                 |

---

## ⚙️ Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/cra9had/userFind.git
cd userFind
```

### 2. Environment setup
Rename `.env.example` to `.env` and fill in the configuration:
```bash
mv .env.example .env
# Set: DATABASE_URL, REDIS_URL, SECRET_KEY, PAYMENT_KEYS, GOOGLE_RECAPTCHA, etc.
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply migrations
```bash
python manage.py migrate
```

### 5. Run Celery worker
```bash
celery -A userFind worker -l info
```

### 6. Run the server
```bash
python manage.py runserver
```

---

## 🔐 Security & User Management

- Google Captcha for registration and login.  
- Password recovery functionality.  
- Trial period for new users.  
- Full vs masked responses for search results depending on subscription/payment.

---

## 💸 Payments

- Card payments via **Payok**.  
- Cryptocurrency payments via **OXAPAY**.  
- Subscription-based and on-demand full access.

---

## 🤝 Contributing

Pull requests are welcome!  
Please ensure code quality and tests pass before submitting.