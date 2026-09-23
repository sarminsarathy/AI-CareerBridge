# AI CareerBridge — Unified Student Career Development Platform

A complete full-stack web application designed to empower students through skill analysis, skill gap calculation, explainable AI career recommendations, industry internship and job matching, rule-based government scheme eligibility evaluation, and personalized career roadmaps with real-time English and Tamil UI support.

---

## 🌟 Key Features

1. **Student Module & Profile Management**:
   - Secure registration & password hashing (PBKDF2 SHA256).
   - HMAC-SHA256 JWT session tokens stored securely in browser `localStorage`.
   - Profile management: Education level, college, course, location, graduation year, career interests.
   - Dynamic skill management: Add/remove skills with categories and proficiency ratings (Beginner, Intermediate, Advanced, Expert).

2. **Deterministic AI Recommendation & Skill Gap Engine**:
   - Skill breakdown into strong, moderate, beginner, and category matrices.
   - Numerical skill gap calculation against target career skill requirements (Software Developer, Data Analyst, AI/ML Engineer, Cybersecurity, Cloud Engineer, UI/UX Designer).
   - Weighted match score calculation and transparent, explainable *"Why Recommended?"* rationale generated dynamically from real student data.

3. **Opportunity Matching Module**:
   - Live dynamic skill match calculation (%) for Internships and Jobs.
   - Breakdown of matching skills and missing skills per opportunity.
   - Direct links to official application portals.

4. **Government Scheme Eligibility Engine**:
   - Rule-based eligibility checker parsing education level, age, state domicile, and income criteria.
   - Returns status (`Eligible`, `Needs Verification`, `Not Eligible`) with transparent evaluation rationale.
   - Required document checklist with interactive status toggles (`Available`, `Not Available`, `Need to Obtain`).
   - Official application URLs for schemes (e.g., Naan Mudhalvan, PM Vidya Lakshmi, AICTE Pragati, Post Matric Scholarship).

5. **Personalized 7-Step Career Roadmap**:
   - Dynamic roadmap generator connecting profile, skill gaps, recommendations, opportunities, and eligible government support into actionable sequential milestones.

6. **Bilingual UI (English | தமிழ்)**:
   - Instant real-time language switcher changing visible headings, form labels, buttons, navigation items, and status indicators without reloading.

---

## 🛠️ Technology Stack

- **Backend**: Python REST API Server (`server.py` using standard library `http.server`).
- **Database**: SQLite (`careerbridge.db`) with relational schema, foreign keys, and indexes.
- **Frontend**: Single Page Application (HTML5, Vanilla CSS3, Vanilla JavaScript ES6+ in `public/`).
- **Security**: PBKDF2 SHA256 password hashing with random salt, HMAC-SHA256 JWT authorization tokens.

---

## 🚀 Local Development Setup

### 1. Initialize & Seed Database
Run the seeding script to create and populate `careerbridge.db` with master skills, career roles, internships, jobs, government schemes, and a demo student account:

```bash
python seed.py
```

### 2. Run Python Full-Stack Backend
Launch the backend server:

```bash
python server.py
```

### 3. Access Application
Open your web browser and navigate to:
[http://localhost:5000/](http://localhost:5000/)

*(The Python backend automatically serves the frontend interface from `public/index.html`).*

---

## 💻 VS Code / Antigravity "Go Live" (Live Server)

You can also run the frontend using Live Server:

1. Right-click [`public/index.html`](file:///c:/Users/sarmi/OneDrive/Desktop/pro/public/index.html) and select **Open with Live Server**, OR click the **Go Live** button in VS Code.
2. The application will open directly at:
   `http://127.0.0.1:5500/` or `http://127.0.0.1:5501/`
3. Make sure the Python backend (`python server.py`) is running on port 5000. The frontend automatically routes API requests to `http://localhost:5000`.

---

## 🌐 GitHub Pages Deployment Guide

GitHub Pages serves static frontend files (HTML, CSS, JavaScript). Because GitHub Pages cannot execute Python backend scripts (`server.py`) or connect directly to a local SQLite database (`careerbridge.db`), the architecture is decoupled as follows:

- **Frontend Hosting**: Hosted on GitHub Pages (`https://sarminsarathy.github.io/AI-CareerBridge/`).
- **Backend Hosting**: Deploy `server.py` to a cloud provider (such as Render, Railway, AWS, Heroku, or Fly.io).

### Configuring Deployed Backend URL in `api.js`:

1. Open [`public/js/api.js`](file:///c:/Users/sarmi/OneDrive/Desktop/pro/public/js/api.js).
2. Locate the `API_CONFIG` object at the top of the file:

```javascript
const API_CONFIG = {
    development: 'http://localhost:5000',
    production: 'YOUR_DEPLOYED_BACKEND_URL' // <-- Replace with your deployed backend URL
};
```

3. Replace `'YOUR_DEPLOYED_BACKEND_URL'` with your live backend domain (e.g. `'https://ai-careerbridge-backend.onrender.com'`).
4. Commit and push your changes to GitHub.
5. In GitHub Repository Settings -> Pages, select Source: `Deploy from a branch` (Branch: `main`, Folder: `/` or `/public`).

When accessed on localhost / Live Server, the app will automatically connect to `http://localhost:5000`. When accessed on GitHub Pages, it will connect to your deployed production backend.

---

## 🔑 Demo Student Credentials

Use the pre-seeded demo account to test the complete end-to-end user journey:

- **Email**: `demo@student.local`
- **Password**: `Demo@12345`

*(Click the **"Use Demo Account"** button on the login screen to auto-fill credentials).*

---

## 📂 Project Structure

```
AI-CareerBridge/
│
├── public/
│   ├── index.html          # Main SPA Frontend Entry
│   ├── css/
│   │   └── main.css        # Clean responsive styling & design tokens
│   └── js/
│       ├── api.js          # API Client & Environment BaseURL Configuration
│       ├── app.js          # Main SPA Application Logic & View Renderers
│       └── i18n.js         # English & Tamil Dictionary & Language Switcher
│
├── src/
│   ├── database.py         # SQLite connection & schema definitions
│   ├── auth.py             # Password hashing (PBKDF2) & JWT token handlers
│   ├── ai_engine.py        # Skill breakdown, skill gap & career recommendation engine
│   ├── eligibility_engine.py # Government scheme rule evaluation engine
│   ├── opportunity_engine.py # Job & internship dynamic match engine
│   └── roadmap_engine.py   # Unified 7-step career roadmap generator
│
├── index.html              # Workspace root redirect helper for Live Server / Pages
├── server.py               # REST API server & static asset host (Port 5000)
├── seed.py                 # Database seeder
├── careerbridge.db         # SQLite database
├── package.json
└── README.md
```
