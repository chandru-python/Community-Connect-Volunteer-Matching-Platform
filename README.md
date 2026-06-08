# Community Connect – Volunteer Matching Platform

## 🌟 Overview

Community Connect is a Flask-based web application that bridges the gap between volunteers and community organizations. The platform enables organizers to create and manage community service projects while allowing volunteers to discover opportunities, apply for projects, and track their participation.

The goal of the platform is to promote social impact by simplifying volunteer engagement and project management.

---

## 🚀 Features

### 👥 Volunteer Features

* User Registration & Login
* Browse Available Projects
* Search Projects by Title
* Filter Projects by Location
* Apply for Volunteer Opportunities
* Track Application Status
* View Personal Dashboard
* Monitor Accepted & Pending Applications

### 🏢 Organizer Features

* Organizer Registration & Login
* Create New Community Projects
* Edit Existing Projects
* Delete Projects
* View Project Applicants
* Accept or Reject Volunteer Applications
* Organizer Dashboard with Statistics

### 🔐 Security Features

* Password Hashing using Werkzeug
* Session-Based Authentication
* Role-Based Access Control
* Protected Routes for Volunteers and Organizers

---

## 🛠️ Technology Stack

### Backend

* Python
* Flask
* SQLAlchemy
* SQLite

### Frontend

* HTML5
* CSS3
* JavaScript
* Bootstrap

### Database

* SQLite Database

---

## 📂 Project Structure

```text
community-connect/
│
├── app.py
├── models.py
├── requirements.txt
├── instance/
│   └── database.db
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── projects.html
│   ├── applications.html
│   ├── volunteer_dashboard.html
│   ├── organizer_dashboard.html
│   ├── applicants.html
│   └── add_project.html
│
└── README.md
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/chandru-python/Community-Connect-Volunteer-Matching-Platform.git

cd Community-Connect-Volunteer-Matching-Platform
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows

```bash
venv\Scripts\activate
```

Linux / Mac

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Application

```bash
python app.py
```

Open your browser and visit:

```text
http://127.0.0.1:5000
```

---

## 📊 System Workflow

1. User registers as Volunteer or Organizer.
2. Organizer creates community projects.
3. Volunteers browse available opportunities.
4. Volunteers apply to projects.
5. Organizers review applications.
6. Applications are Accepted, Rejected, or Kept Pending.
7. Users monitor activities through personalized dashboards.

---

## 🎯 Future Enhancements

* Email Notifications
* Volunteer Recommendation System
* Project Rating & Feedback
* Real-Time Chat
* Certificate Generation
* AI-Based Volunteer Matching
* Cloud Deployment (AWS/Azure)

---

## 🤝 Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to GitHub
5. Open a Pull Request

---

## 📜 License

This project is developed for educational and community engagement purposes.

---

## 👨‍💻 Author

**Chandru M**

AI/ML Engineer | Python Developer

GitHub: https://github.com/chandru-python

---

⭐ If you found this project useful, consider giving it a star on GitHub.
