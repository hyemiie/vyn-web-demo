# Vyn – Web Backend 

This is the **backend server** for **Vyn**, an AI-powered code security scanner that analyzes codebases for vulnerabilities and returns actionable insights to the [frontend interface](https://vyn-web-scanner.onrender.com/hero).

> **Frontend repository**: [vyn-frontend-repo](https://github.com/hyemiie/vyn_web_scanner)

## How It works

Vyn accepts public GitHub repositories through the frontend and scans the codebase for potential security vulnerabilities. The backend processes each scan and uses a large language model (LLM) to analyze detected issues, assign severity levels, and generate actionable recommendations. 

### The backend is responsible for:

- Accepting and processing public code repositories  
- Analyzing repositories for potential security vulnerabilities  
- Structuring vulnerability data and sending it to an LLM using optimized prompts  
- Interpreting LLM responses to generate fix suggestions, classified by severity (critical, high, medium, low)  
- Serving scan results to the frontend through a REST API  

---

## Technologies Used
**Backend**: Python, Django

**AI Integration**: OpenAI’s LLM 

**Scanning /Analysis:** Bandit

**Frontend (in a separate repo):** Next.js
  

## How to Set Up the Server Locally

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


## Connect
I'm always open to feedback and suggestions, you can reach me at 

GitHub: [@hyemiie](https://github.com/hyemiie)  
Frontend Repository: [Vyn-frontend](https://github.com/hyemiie/vyn_web_scanner)  
Email: yemiojedapo1@gmail.com


