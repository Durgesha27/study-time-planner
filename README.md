# 📚 Study Time Planner

A web-based **Study Time Planner** designed to help students organize their study activities, create goals, manage schedules, and monitor their academic progress.

The application provides a simple and user-friendly interface for planning study sessions and tracking progress from a centralized dashboard.

---

## 🚀 Features

### 📊 Dashboard

The dashboard provides an overview of the student's study activities and progress.

Users can view:

* Study statistics
* Recent activities
* Weekly study information
* Current goals
* Progress information

---

### 🎯 Goals

The Goals section allows students to create and manage study goals.

Users can:

* Add a new goal
* Set a target or deadline
* Track goal progress
* Update progress using a progress slider
* Delete completed or unnecessary goals

Example:

```text
Goal: Complete Mathematics Chapter 5
Target: By September 30
Progress: 65%
```

---

### 📅 Schedule

The Schedule section helps students organize their study activities.

Users can:

* Create study schedules
* Specify study subjects
* Set dates and times
* Organize study sessions
* View planned study activities

---

### 📈 Progress Tracking

The Progress section allows users to monitor their study performance.

It can display:

* Daily study hours
* Weekly study hours
* Completed tasks
* Goal progress
* Study statistics

---

### 👤 Profile

The Profile section provides information about the current user and their account.

---

## 🛠️ Technologies Used

### Frontend

* HTML5
* CSS3
* JavaScript
* Jinja2 Templates

### Backend

* Python
* Flask
* Flask API routes

### Database

* SQLite / project database

### Development Tools

* Git
* GitHub
* Visual Studio Code

---
###PROJECT STRUCTURE
study-time-planner/
│
├── .gitignore
├── study time planner.py
│
└── templates/
    ├── goals.html
    ├── home.html
    ├── loginsignup.html
    ├── profile.html
    └── schedule.html


## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Durgesha27/study-time-planner.git
```

### 2. Open the project directory

```bash
cd study-time-planner
```

### 3. Create a virtual environment

Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
python app.py
```

The application will normally be available at:

```text
http://127.0.0.1:5000/
```

---

## 🎯 Goal Management

The Goals module provides functionality for creating and tracking study goals.

The basic workflow is:

```text
User
  ↓
Click "Add Goal"
  ↓
Enter Goal Title
  ↓
Enter Target / Deadline
  ↓
Click "Add Goal"
  ↓
Frontend sends goal data
  ↓
Backend Goal API
  ↓
Database
  ↓
Goal displayed on Goals page
```

A goal request can contain information such as:

```json
{
    "title": "Complete Mathematics",
    "target_hours": 20
}
```

The backend processes the request and stores the goal.

---

## 🔌 API

The application uses backend API routes to communicate between the frontend and backend.

Example goal request:

```http
POST /api/goals
Content-Type: application/json
```

Example request body:

```json
{
    "title": "Complete Mathematics",
    "target_hours": 20
}
```

The frontend can send the request using JavaScript:

```javascript
fetch("/api/goals", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify({
        title: title,
        target_hours: targetHours
    })
});
```

---

## 🖥️ User Interface

The application contains the following main pages:

| Page     | Purpose                      |
| -------- | ---------------------------- |
| Home     | Dashboard and study overview |
| Schedule | Manage study schedules       |
| Progress | View study statistics        |
| Goals    | Create and track goals       |
| Profile  | Manage user information      |

The interface uses a consistent design across the different pages to make navigation easier.

---

## 🔄 Application Architecture

The application follows a basic three-layer architecture:

```text
┌─────────────────────────────┐
│        User Interface       │
│     HTML / CSS / JavaScript │
└──────────────┬──────────────┘
               │
               │ HTTP / API
               ▼
┌─────────────────────────────┐
│       Flask Backend         │
│     Routes / API Logic      │
└──────────────┬──────────────┘
               │
               │ Database Queries
               ▼
┌─────────────────────────────┐
│          Database           │
│       SQLite / DB Layer     │
└─────────────────────────────┘
```

---

## 📌 Main Modules

### Home Module

Responsible for displaying the main dashboard and summary information.

### Schedule Module

Responsible for creating and managing study schedules.

### Goals Module

Responsible for:

* Creating goals
* Updating goal progress
* Deleting goals
* Displaying goal information

### Progress Module

Responsible for calculating and displaying study progress and statistics.

### Profile Module

Responsible for displaying and managing user profile information.

---

## 🧪 Testing

Before using the application, test the following functionality:

* User can open the home page
* Navigation works correctly
* User can create a study goal
* User can update goal progress
* User can delete a goal
* Schedule entries can be created
* Progress information is displayed correctly
* Backend API requests return the expected response
* Invalid form submissions are handled correctly

---

## 🔮 Future Enhancements

Possible future improvements include:

1. User authentication and authorization
2. Cloud database support
3. Study reminders and notifications
4. Calendar integration
5. Advanced study analytics
6. Subject-wise progress tracking
7. Study streak tracking
8. Mobile-responsive improvements
9. Export study reports
10. Automated study-plan generation

---

---

## 👨‍💻 Project

**Project Name:** Study Time Planner

**Repository:**
https://github.com/Durgesha27/study-time-planner

**Purpose:**
To provide students with a centralized web application for planning study activities, setting goals, managing schedules, and tracking academic progress.
