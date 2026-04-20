# Team4-CS321 - GameHub

A web-based gaming platform built with Django featuring multiple interactive games, user authentication, email notifications, and game analytics.

## 🎮 Features

- **4 Interactive Games:** Hangman, Snake, Tic-Tac-Toe, and Mind Mosaic
- **User Authentication:** Secure login and registration system
- **Leaderboard System:** Track and compete with per-user score rankings
- **Game Analytics:** Track play history and high scores
- **Email Notifications:** Automated reminders to keep users engaged
- **User Preferences:** Customizable notification settings
- **Admin Panel:** Full administrative interface for data management

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/dudette909/Team4-CS321
cd Team4-CS321/myproject

# Install all dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start the development server
python manage.py runserver
```

Visit: **http://127.0.0.1:8000/**


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
- Score: Based on remaining attempts (max 60 points)

### 🐍 Snake
- Canvas-based rendering
- Collision detection
- Dynamic speed increases
- Score: 10 points per food eaten

### ⭕ Tic-Tac-Toe
- Player vs Computer AI
- Multiple difficulty levels
- Win detection algorithm
- Score: Win = 100, Tie = 50, Loss = 0

### 🧩 Mind Mosaic
- Sliding puzzle game
- Multiple grid sizes (3x3, 4x4, 5x5)
- Hint system and magic shuffle
- Score: Based on moves (fewer = better, max 1000 points)

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


