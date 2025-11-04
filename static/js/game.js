// Spider-Guesser Game Logic

let currentGameId = null;
let selectedDifficulty = 'easy';
let gameData = {};

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setupDifficultyButtons();
    setupStartForm();
    setupGuessForm();
});

// Difficulty Button Selection
function setupDifficultyButtons() {
    const buttons = document.querySelectorAll('.difficulty-btn');
    
    buttons.forEach(btn => {
        btn.addEventListener('click', () => {
            buttons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            selectedDifficulty = btn.dataset.difficulty;
        });
    });
}

// Start Game Form
function setupStartForm() {
    const form = document.getElementById('startGameForm');
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const playerName = document.getElementById('playerName').value.trim();
        
        if (!playerName) {
            alert('Please enter your hero name!');
            return;
        }
        
        await startGame(playerName, selectedDifficulty);
    });
}

// Guess Form
function setupGuessForm() {
    const form = document.getElementById('guessForm');
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const guessInput = document.getElementById('guessInput');
        const guess = parseInt(guessInput.value);
        
        if (isNaN(guess)) {
            showHint('Please enter a valid number! 🕷️');
            return;
        }
        
        await makeGuess(guess);
        guessInput.value = '';
        guessInput.focus();
    });
}

// API: Start Game
async function startGame(playerName, difficulty) {
    try {
        const response = await fetch('/game/start', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                player_name: playerName,
                difficulty: difficulty
            })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            alert(data.error || 'Failed to start game');
            return;
        }
        
        currentGameId = data.game_id;
        gameData = {
            playerName: playerName,
            difficulty: difficulty,
            maxAttempts: data.max_attempts,
            attemptsUsed: 0
        };
        
        showGameScreen();
        
    } catch (error) {
        console.error('Error starting game:', error);
        alert('Failed to connect to server. Please try again.');
    }
}

// API: Make Guess
async function makeGuess(guess) {
    try {
        const response = await fetch(`/game/${currentGameId}/guess`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ guess: guess })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            showHint(data.error || 'Invalid guess');
            return;
        }
        
        gameData.attemptsUsed++;
        updateAttemptsDisplay();
        
        // Add guess to list
        addGuessToList(guess, data.hint || 'checking...');
        
        // Handle result
        if (data.result === 'win') {
            showResultScreen(true, data);
        } else if (data.result === 'lose') {
            showResultScreen(false, data);
        } else {
            showHint(data.hint);
        }
        
    } catch (error) {
        console.error('Error making guess:', error);
        showHint('Connection error. Please try again.');
    }
}

// API: Get Leaderboard
async function loadLeaderboard() {
    try {
        const response = await fetch('/leaderboard');
        const data = await response.json();
        
        displayLeaderboard(data.leaderboard || []);
        
    } catch (error) {
        console.error('Error loading leaderboard:', error);
        document.getElementById('leaderboardList').innerHTML = 
            '<div class="loading">Failed to load leaderboard</div>';
    }
}

// UI: Show Game Screen
function showGameScreen() {
    document.getElementById('setupScreen').classList.remove('active');
    document.getElementById('gameScreen').classList.add('active');
    
    document.getElementById('displayPlayerName').textContent = gameData.playerName;
    document.getElementById('displayDifficulty').textContent = 
        gameData.difficulty.charAt(0).toUpperCase() + gameData.difficulty.slice(1);
    
    const ranges = {
        easy: '1-50',
        medium: '1-100',
        hard: '1-200'
    };
    document.getElementById('displayRange').textContent = ranges[gameData.difficulty];
    
    document.getElementById('maxAttempts').textContent = gameData.maxAttempts;
    updateAttemptsDisplay();
    
    document.getElementById('guessInput').focus();
}

// UI: Update Attempts Display
function updateAttemptsDisplay() {
    const remaining = gameData.maxAttempts - gameData.attemptsUsed;
    document.getElementById('attemptsRemaining').textContent = remaining;
}

// UI: Show Hint
function showHint(hint) {
    const hintBox = document.getElementById('hintBox');
    const hintText = document.getElementById('hintText');
    
    hintText.textContent = hint;
    hintBox.classList.remove('hidden');
    
    // Add animation
    hintBox.style.animation = 'none';
    setTimeout(() => {
        hintBox.style.animation = 'slideIn 0.4s ease';
    }, 10);
}

// UI: Add Guess to List
function addGuessToList(guess, hint) {
    const guessList = document.getElementById('guessList');
    
    const guessItem = document.createElement('div');
    guessItem.className = 'guess-item';
    guessItem.innerHTML = `
        <span class="guess-number">🎯 Attempt ${gameData.attemptsUsed}: ${guess}</span>
        <span class="guess-hint">${hint}</span>
    `;
    
    guessList.insertBefore(guessItem, guessList.firstChild);
}

// UI: Show Result Screen
function showResultScreen(won, data) {
    document.getElementById('gameScreen').classList.remove('active');
    document.getElementById('resultScreen').classList.add('active');
    
    const resultEmoji = document.getElementById('resultEmoji');
    const resultTitle = document.getElementById('resultTitle');
    const resultMessage = document.getElementById('resultMessage');
    const scoreDisplay = document.getElementById('scoreDisplay');
    const finalScore = document.getElementById('finalScore');
    
    if (won) {
        resultEmoji.textContent = '🎉';
        resultTitle.textContent = 'MISSION ACCOMPLISHED!';
        resultMessage.textContent = 'Great job, web-slinger! You guessed it!';
        scoreDisplay.classList.remove('hidden');
        finalScore.textContent = data.score || 0;
    } else {
        resultEmoji.textContent = '😢';
        resultTitle.textContent = 'MISSION FAILED';
        resultMessage.textContent = 'Out of web shots! Better luck next time!';
        scoreDisplay.classList.add('hidden');
    }
    
    document.getElementById('targetNumber').textContent = data.target_number;
    document.getElementById('totalAttempts').textContent = data.attempts;
}

// UI: Toggle Leaderboard
function toggleLeaderboard() {
    const popup = document.getElementById('leaderboardPopup');
    
    if (popup.classList.contains('hidden')) {
        popup.classList.remove('hidden');
        loadLeaderboard();
    } else {
        popup.classList.add('hidden');
    }
}

// UI: Display Leaderboard
function displayLeaderboard(leaderboard) {
    const list = document.getElementById('leaderboardList');
    
    if (leaderboard.length === 0) {
        list.innerHTML = '<div class="loading">No heroes yet. Be the first!</div>';
        return;
    }
    
    list.innerHTML = '';
    
    leaderboard.forEach((entry, index) => {
        const item = document.createElement('div');
        item.className = 'leaderboard-item';
        
        const medals = ['🥇', '🥈', '🥉'];
        const rank = index < 3 ? medals[index] : `#${index + 1}`;
        
        item.innerHTML = `
            <div class="leaderboard-rank">${rank}</div>
            <div class="leaderboard-info">
                <div class="leaderboard-name">${entry.player_name}</div>
                <div class="leaderboard-details">
                    ${entry.difficulty} • ${entry.attempts} attempts
                </div>
            </div>
            <div class="leaderboard-score">${entry.score}</div>
        `;
        
        list.appendChild(item);
    });
}

// Restart Game
function restartGame() {
    currentGameId = null;
    gameData = {};
    selectedDifficulty = 'easy';
    
    document.getElementById('resultScreen').classList.remove('active');
    document.getElementById('setupScreen').classList.add('active');
    
    document.getElementById('playerName').value = '';
    document.getElementById('guessList').innerHTML = '';
    document.getElementById('hintBox').classList.add('hidden');
    
    // Reset difficulty buttons
    document.querySelectorAll('.difficulty-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.difficulty === 'easy') {
            btn.classList.add('active');
        }
    });
}