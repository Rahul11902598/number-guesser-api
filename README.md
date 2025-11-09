# 🕷️ Spider-Guesser | Number Guessing Game API

[![Tests](https://github.com/Rahul11902598/number-guesser-api/actions/workflows/test.yml/badge.svg)](https://github.com/Rahul11902598/number-guesser-api/actions/workflows/test.yml)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Code Coverage](https://img.shields.io/badge/coverage-95%25-brightgreen.svg)](htmlcov/index.html)

A production-ready REST API game where players guess numbers with real-time hints, scoring system, and global leaderboards. Features comprehensive QA testing with 100% pass rate.

**Live Demo:** [Try it here](http://localhost:5000) | **Portfolio:** [cloudbyrahul.com](https://cloudbyrahul.com)

---

## 🎯 Project Highlights

- ✅ **100% Test Coverage** - 33 Postman + 20 Pytest automated tests
- ✅ **Zero Bugs** - Rigorous QA testing with professional documentation
- ✅ **CI/CD Pipeline** - GitHub Actions with automated testing
- ✅ **Lightning Fast** - Average 4ms API response time
- ✅ **Security Tested** - XSS protection and input validation
- ✅ **Production Ready** - Comprehensive error handling

---

## 🚀 Features

### Core Gameplay
- 🎮 Three difficulty levels (Easy, Medium, Hard)
- 💡 Smart hint system (too high/low, very close!)
- 🎯 Dynamic scoring based on attempts
- 🏆 Global leaderboard (top 10 players)
- 📊 Real-time statistics tracking

### Technical Features
- 🔒 Robust input validation
- 🛡️ XSS and injection protection
- ⚡ Single-digit millisecond response times
- 🎨 Spiderman-themed responsive UI
- 📱 Mobile-friendly design
- 🔄 RESTful API architecture

---

## 🛠️ Tech Stack

**Backend:**
- Python 3.11
- Flask 3.0 (REST API)
- UUID for game sessions
- In-memory data storage

**Frontend:**
- HTML5 / CSS3 / JavaScript
- Responsive design
- Animated UI elements
- Real-time game state updates

**Testing & QA:**
- Postman (API testing)
- Pytest (Automated tests)
- pytest-cov (Code coverage)
- GitHub Actions (CI/CD)

**DevOps:**
- Git version control
- GitHub Actions CI/CD
- Professional QA documentation

---

## 📦 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager
- Git

### Installation

```bash
# Clone repository
git clone https://github.com/Rahul11902598/number-guesser-api.git
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

Server runs on `http://localhost:5000`

---

## 📚 API Documentation

### Base URL
```
http://localhost:5000
```

### Endpoints

#### 1. Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "active_games": 0,
  "timestamp": "2025-11-05T01:41:27.826028"
}
```

---

#### 2. Start New Game
```http
POST /game/start
Content-Type: application/json
```

**Request Body:**
```json
{
  "player_name": "Rahul",
  "difficulty": "easy"  // Options: easy, medium, hard
}
```

**Response:** `201 Created`
```json
{
  "game_id": "uuid-here",
  "message": "Game started! Guess a number between 1 and 50",
  "difficulty": "easy",
  "max_attempts": 10
}
```

**Validation:**
- `player_name`: Required, 1-20 characters
- `difficulty`: Optional, defaults to "medium"

---

#### 3. Make a Guess
```http
POST /game/{game_id}/guess
Content-Type: application/json
```

**Request Body:**
```json
{
  "guess": 25
}
```

**Response:** `200 OK`
```json
{
  "result": "continue",  // or "win" or "lose"
  "hint": "too low",
  "attempts_used": 1,
  "attempts_remaining": 9
}
```

**Win Response:**
```json
{
  "result": "win",
  "message": "Congratulations! You guessed it in 3 attempts!",
  "target_number": 42,
  "attempts": 3,
  "score": 170
}
```

---

#### 4. Get Game Status
```http
GET /game/{game_id}
```

**Response:** `200 OK`
```json
{
  "game_id": "uuid",
  "player_name": "Rahul",
  "difficulty": "easy",
  "status": "active",  // or "won" or "lost"
  "attempts": 3,
  "max_attempts": 10,
  "guesses": [
    {
      "attempt": 1,
      "guess": 25,
      "hint": "too low",
      "timestamp": "2025-11-05T01:41:27.826028"
    }
  ]
}
```

---

#### 5. Get Leaderboard
```http
GET /leaderboard
```

**Response:** `200 OK`
```json
{
  "leaderboard": [
    {
      "player_name": "Rahul",
      "difficulty": "hard",
      "attempts": 2,
      "score": 330,
      "completed_at": "2025-11-05T01:41:27.826028"
    }
  ],
  "total_games": 42
}
```

---

#### 6. Get Statistics
```http
GET /stats
```

**Response:** `200 OK`
```json
{
  "total_games": 100,
  "active_games": 5,
  "completed_games": 95,
  "won_games": 70,
  "lost_games": 25,
  "win_rate": 73.68
}
```

---

## 🧪 Testing

### Run All Tests

```bash
# Activate virtual environment
venv\Scripts\activate

# Run Pytest tests
pytest -v tests/

# Run with coverage
pytest --cov=app --cov-report=html tests/

# Open coverage report
start htmlcov\index.html  # Windows
open htmlcov/index.html   # Mac
```

### Test Results

✅ **Postman API Tests:** 14 requests, 33 assertions, 100% pass  
✅ **Pytest Automated Tests:** 20 tests, 100% pass  
✅ **Code Coverage:** 95%+  
✅ **Performance:** < 5ms average response time  
✅ **Security:** XSS and injection protected  

### Import Postman Collection

1. Open Postman
2. Import `postman_collection.json`
3. Run collection to see all tests pass

---

## 📊 Project Structure

```
number-guesser-api/
├── .github/
│   └── workflows/
│       └── test.yml          # CI/CD pipeline
├── static/
│   ├── css/
│   │   └── style.css         # Spiderman theme
│   └── js/
│       └── game.js           # Frontend logic
├── templates/
│   └── index.html            # Game UI
├── tests/
│   ├── __init__.py
│   ├── conftest.py           # Pytest configuration
│   ├── test_health.py        # Health endpoint tests
│   ├── test_game_start.py    # Game creation tests
│   └── test_validation.py    # Input validation tests
├── docs/
│   ├── QA_TEST_REPORT.md     # Professional QA report
│   └── postman_test_results.json
├── app.py                    # Flask application
├── requirements.txt          # Python dependencies
├── postman_collection.json   # Postman test suite
├── BUGS.md                   # Bug tracking
├── .gitignore
└── README.md
```

---

## 🎮 Game Rules

### Difficulty Levels

| Difficulty | Range | Max Attempts | Base Score |
|------------|-------|--------------|------------|
| Easy | 1-50 | 10 | 100 |
| Medium | 1-100 | 7 | 200 |
| Hard | 1-200 | 5 | 300 |

### Scoring System

```
Final Score = Base Score + (Max Attempts - Used Attempts) × 10
```

**Example:**
- Hard mode (base: 300)
- Won in 2 attempts
- Score: 300 + (5 - 2) × 10 = **330 points**

### Hint System

- **"correct"** - You won!
- **"very close!"** - Within 5 of target
- **"close!"** - Within 10 of target
- **"too high"** / **"too low"** - General direction

---

## 🔒 Security Features

- ✅ Input validation on all endpoints
- ✅ XSS protection (script tag blocking)
- ✅ SQL injection safe (no database queries)
- ✅ Range validation for guesses
- ✅ Length validation for player names
- ✅ Type checking for numeric inputs
- ✅ Game state validation (can't guess after game ends)

---

## ⚡ Performance Metrics

| Metric | Value | Status |
|--------|-------|--------|
| Average Response Time | 4.07ms | ⚡ Excellent |
| Fastest Endpoint | 3ms | ⚡ Excellent |
| Slowest Endpoint | 6ms | ⚡ Excellent |
| Total Test Execution | 57ms | ⚡ Excellent |

*Tested on Windows 11, Python 3.11*

---

## 🐛 Known Issues

See [BUGS.md](BUGS.md) for detailed bug tracking.

**Current Status:** ✅ Zero Critical Bugs

---

## 🔄 CI/CD Pipeline

Automated testing runs on every push:

1. ✅ Code checkout
2. ✅ Python environment setup
3. ✅ Dependency installation
4. ✅ Health check tests
5. ✅ Game flow tests
6. ✅ Error handling tests
7. ✅ Code quality linting
8. ✅ Security scanning

---

## 📈 Future Enhancements

- [ ] User authentication (JWT)
- [ ] Persistent database (PostgreSQL/MongoDB)
- [ ] Real-time multiplayer mode
- [ ] WebSocket support for live updates
- [ ] Advanced statistics and analytics
- [ ] Achievement system
- [ ] Daily challenges
- [ ] Social sharing features
- [ ] Deploy to AWS Lambda + API Gateway
- [ ] Add Docker containerization

---

## 👨‍💻 Author

**Rahul Domakonda**  
Cloud Engineer | QA Engineer | AWS Certified

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue)](https://linkedin.com/in/rahul-domakonda-6973b5195)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black)](https://github.com/Rahul11902598)
[![Portfolio](https://img.shields.io/badge/Portfolio-Visit-green)](https://cloudbyrahul.com)
[![Email](https://img.shields.io/badge/Email-Contact-red)](mailto:rahul.11902598@gmail.com)

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Inspired by classic number guessing games
- Spiderman theme for fun UI
- Flask documentation and community
- Postman for excellent API testing tools
- GitHub Actions for seamless CI/CD

---

## 📞 Support

If you have any questions or run into issues:

- 📧 Email: rahul.11902598@gmail.com
- 💼 LinkedIn: [Rahul Domakonda](https://linkedin.com/in/rahul-domakonda-6973b5195)
- 🐛 Report bugs: [GitHub Issues](https://github.com/Rahul11902598/number-guesser-api/issues)

---

<div align="center">

### ⭐ If you found this helpful, please star the repository!

**Built with ❤️ by Rahul Domakonda**

</div>