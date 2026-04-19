# Team4-CS321 - GameHub

A web-based gaming platform built with Django featuring multiple interactive games, user authentication, email notifications, and game analytics.

## 🎮 Features

- **3 Interactive Games:** Hangman, Snake, and Tic-Tac-Toe
- **User Authentication:** Secure login and registration system
- **Game Analytics:** Track play history and high scores
- **Email Notifications:** Automated reminders to keep users engaged
- **User Preferences:** Customizable notification settings
- **Admin Panel:** Full administrative interface for data management

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/Team4-CS321.git
cd Team4-CS321/myproject

# Install all dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start the development server
python manage.py runserver
```

Visit: **http://127.0.0.1:8000/**

📖 **[Full Installation Guide](myproject/INSTALLATION.md)** - Detailed setup instructions, troubleshooting, and virtual environment setup

## 📋 Requirements

All dependencies are listed in [`requirements.txt`](myproject/requirements.txt):

- Django 5.1.1
- python-dotenv 1.0.1
- Pillow 12.1.1
- And all Django dependencies

**One command installs everything:**
```bash
pip install -r requirements.txt
```

## 📁 Project Structure

```
Team4-CS321/
├── myproject/                  # Django project root
│   ├── main/                   # Main application
│   │   ├── models.py          # Database models
│   │   ├── views.py           # View functions
│   │   ├── admin.py           # Admin configuration
│   │   ├── templates/         # HTML templates
│   │   └── static/            # CSS, JS, images
│   ├── myproject/             # Project settings
│   │   ├── settings.py        # Configuration
│   │   └── urls.py            # URL routing
│   ├── requirements.txt       # Python dependencies
│   ├── .env.example          # Environment variables template
│   └── manage.py             # Django management script
├── docs/                      # Project documentation
│   ├── PROJECT_DOCUMENTATION.md
│   └── BUG_FIXES_SUMMARY.md
└── README.md                  # This file
```

## 👥 Team Members

- **Abhisek Bhujel** - Primary Developer (Dashboard, Games, Authentication, Email)
- **trinity** - Database Architect (Models, Migrations, Virtual Buddy)
- **Jj00703** - Project Manager (Setup, Configuration, Documentation, Bug Fixes)
- **dudette909** - Media Manager (Assets, Testing Support)

## 📚 Documentation

- **[Project Documentation](docs/PROJECT_DOCUMENTATION.md)** - Complete project deliverable documentation
- **[Bug Fixes Summary](docs/BUG_FIXES_SUMMARY.md)** - Recent improvements and fixes
- **[Installation Guide](myproject/INSTALLATION.md)** - Detailed setup instructions
- **[Environment Setup](myproject/ENV_SETUP.md)** - Environment variables guide

## 🛠️ Technologies Used

- **Backend:** Django 5.1.1, Python 3.12, SQLite
- **Frontend:** Bootstrap 5.3.8, Vanilla JavaScript, Vanta.js
- **Email:** Gmail SMTP
- **Version Control:** Git/GitHub

## 🎯 Games

### 🔤 Hangman
- Multiple difficulty levels
- Category-based word selection
- Letter tracking system

### 🐍 Snake
- Canvas-based rendering
- Collision detection
- Score tracking

### ⭕ Tic-Tac-Toe
- Player vs Computer AI
- Multiple difficulty levels
- Win detection algorithm

## 🔧 Development

### Create Superuser (Admin Access)

```bash
python manage.py createsuperuser
```

Access admin panel at: **http://127.0.0.1:8000/admin/**

### Run Tests

```bash
python manage.py test
```

### Environment Variables

Copy `.env.example` to `.env` and configure:

```env
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

**Note:** The app works with defaults even without `.env` file!

## 📊 Project Statistics

- **Total Hours:** ~210-230 hours
- **Git Commits:** 15+ commits
- **Lines of Code:** ~2000+ lines
- **Team Members:** 4

## 🔒 Security

- Environment variable support for sensitive data
- CSRF protection enabled
- Password validation
- Secure session management
- `.env` file excluded from version control

## 📝 License

See [LICENSE.md](LICENSE.md) for details.

## 🤝 Contributing

This is a class project for CS 321 - Software Engineering.

## 📧 Contact

For questions about this project, contact the team members through the course channels.

---

**CS 321 - Software Engineering**  
**Last Updated:** April 19, 2026
