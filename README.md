# 🎮 Number Guesser Pro API

A simple REST API game where players guess numbers with scoring and leaderboards.

## 🚀 Features
- Multiple difficulty levels (Easy, Medium, Hard)
- Real-time hint system
- Score calculation based on attempts
- Global leaderboard
- Game statistics

## 🛠️ Tech Stack
- Python 3.x
- Flask 3.0
- REST API

## 📦 Installation

### Prerequisites
- Python 3.8+
- pip

### Setup
```bash
# Clone repository
git clone <your-repo-url>
cd number-guesser-api

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py
```

API runs on `http://localhost:5000`

## 📚 API Endpoints

### Start Game
```http
POST /game/start
Content-Type: application/json

{
  "player_name": "Rahul",
  "difficulty": "easy"  // easy, medium, hard
}
```

### Make Guess
```http
POST /game/{game_id}/guess
Content-Type: application/json

{
  "guess": 42
}
```

### Get Game Status
```http
GET /game/{game_id}
```

### Leaderboard
```http
GET /leaderboard
```

### Statistics
```http
GET /stats
```

### Health Check
```http
GET /health
```

## 🧪 Testing
Coming soon: Pytest test suite, Postman collection

## 🔄 CI/CD
Coming soon: GitHub Actions pipeline

## 👨‍💻 Author
Rahul Domakonda - [LinkedIn](https://linkedin.com/in/rahul-domakonda-6973b5195) | [GitHub](https://github.com/Rahul11902598)

## 📝 License
MIT License