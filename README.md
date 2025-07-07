# Vyn – Web Backend 🛡️

This is the **backend server** for **Vyn**, an AI-powered code security scanner that analyzes codebases for vulnerabilities and returns actionable insights.


This repo contains the **Django backend**, which handles vulnerability scans, stores results, and serves data to the [frontend interface](https://vyn-web-scanner.onrender.com/hero).

> 🔗 **Frontend repository**: [vyn-frontend-demo](https://github.com/hyemiie/vyn_web_scanner)

---

## 🔧 Features

- ⚙️ Django-based web backend
- 🧠 Handles AI-generated vulnerability scanning results
- 🔐 API endpoints to fetch scan results
- 🌱 Easily extensible and modular architecture

---


## 🧱 Tech Stack Used
- *Backend*: Python, Django
- *API Format*: JSON
- *Frontend (in a separate repo)*: Nextjs
  

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/hyemiie/vyn-web-demo.git
cd vyn-web-demo
```

### 2. Set up virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply migrations
```bash
python manage.py migrate
```

### 5. Run the development server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000` to verify the backend is running.


## 🤝 Connect
I'm always open to feedback and suggestions, you can reach me at 

GitHub: [@hyemiie](https://github.com/hyemiie)  
Frontend Repository: [Vyn-frontend](https://github.com/hyemiie/vyn_web_scanner)  
Email: yemiojedapo1@gmail.com


