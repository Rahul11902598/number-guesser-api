# app.py - Number Guesser Pro API
from flask import Flask, request, jsonify, render_template
from datetime import datetime
import random
import uuid

app = Flask(__name__)

# In-memory storage (resets on restart)
games = {}  # game_id: game_data
leaderboard = []  # list of completed games

# Game difficulty settings
DIFFICULTY = {
    'easy': {'min': 1, 'max': 50, 'max_attempts': 10},
    'medium': {'min': 1, 'max': 100, 'max_attempts': 7},
    'hard': {'min': 1, 'max': 200, 'max_attempts': 5}
}

# Helper Functions
def calculate_score(attempts, difficulty, won):
    """Calculate score based on attempts and difficulty"""
    if not won:
        return 0
    
    base_score = {'easy': 100, 'medium': 200, 'hard': 300}
    max_attempts = DIFFICULTY[difficulty]['max_attempts']
    
    # Better score for fewer attempts
    attempt_bonus = (max_attempts - attempts) * 10
    return base_score[difficulty] + attempt_bonus

def get_hint(guess, target):
    """Generate hint based on guess"""
    diff = abs(guess - target)
    
    if guess == target:
        return "correct"
    elif diff <= 5:
        return "very close! " + ("too high" if guess > target else "too low")
    elif diff <= 10:
        return "close! " + ("too high" if guess > target else "too low")
    else:
        return "too high" if guess > target else "too low"

# Web Routes
@app.route('/')
def index():
    """Serve the main game page"""
    return render_template('index.html')

# API Endpoints

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'active_games': len(games),
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/game/start', methods=['POST'])
def start_game():
    """Start a new game"""
    data = request.get_json() or {}
    
    # Validate difficulty
    difficulty = data.get('difficulty', 'medium').lower()
    if difficulty not in DIFFICULTY:
        return jsonify({
            'error': 'Invalid difficulty',
            'valid_options': list(DIFFICULTY.keys())
        }), 400
    
    # Validate player name
    player_name = data.get('player_name', '').strip()
    if not player_name:
        return jsonify({'error': 'player_name is required'}), 400
    
    if len(player_name) > 20:
        return jsonify({'error': 'player_name must be 20 characters or less'}), 400
    
    # Create new game
    game_id = str(uuid.uuid4())
    settings = DIFFICULTY[difficulty]
    target_number = random.randint(settings['min'], settings['max'])
    
    games[game_id] = {
        'game_id': game_id,
        'player_name': player_name,
        'difficulty': difficulty,
        'target_number': target_number,
        'min_range': settings['min'],
        'max_range': settings['max'],
        'max_attempts': settings['max_attempts'],
        'attempts': 0,
        'guesses': [],
        'status': 'active',
        'started_at': datetime.now().isoformat()
    }
    
    return jsonify({
        'game_id': game_id,
        'message': f'Game started! Guess a number between {settings["min"]} and {settings["max"]}',
        'difficulty': difficulty,
        'max_attempts': settings['max_attempts']
    }), 201

@app.route('/game/<game_id>/guess', methods=['POST'])
def make_guess(game_id):
    """Make a guess in an active game"""
    
    # Check if game exists
    if game_id not in games:
        return jsonify({'error': 'Game not found'}), 404
    
    game = games[game_id]
    
    # Check if game is still active
    if game['status'] != 'active':
        return jsonify({
            'error': 'Game is not active',
            'status': game['status']
        }), 400
    
    # Get and validate guess
    data = request.get_json() or {}
    
    try:
        guess = int(data.get('guess'))
    except (TypeError, ValueError):
        return jsonify({'error': 'guess must be a valid integer'}), 400
    
    # Check if guess is in valid range
    if guess < game['min_range'] or guess > game['max_range']:
        return jsonify({
            'error': f'guess must be between {game["min_range"]} and {game["max_range"]}'
        }), 400
    
    # Process guess
    game['attempts'] += 1
    hint = get_hint(guess, game['target_number'])
    
    game['guesses'].append({
        'attempt': game['attempts'],
        'guess': guess,
        'hint': hint,
        'timestamp': datetime.now().isoformat()
    })
    
    # Check win condition
    if guess == game['target_number']:
        game['status'] = 'won'
        game['ended_at'] = datetime.now().isoformat()
        score = calculate_score(game['attempts'], game['difficulty'], True)
        game['score'] = score
        
        # Add to leaderboard
        leaderboard.append({
            'player_name': game['player_name'],
            'difficulty': game['difficulty'],
            'attempts': game['attempts'],
            'score': score,
            'completed_at': game['ended_at']
        })
        
        return jsonify({
            'result': 'win',
            'message': f'Congratulations! You guessed it in {game["attempts"]} attempts!',
            'target_number': game['target_number'],
            'attempts': game['attempts'],
            'score': score
        }), 200
    
    # Check lose condition
    if game['attempts'] >= game['max_attempts']:
        game['status'] = 'lost'
        game['ended_at'] = datetime.now().isoformat()
        game['score'] = 0
        
        return jsonify({
            'result': 'lose',
            'message': 'Game over! You ran out of attempts.',
            'target_number': game['target_number'],
            'attempts': game['attempts']
        }), 200
    
    # Continue playing
    return jsonify({
        'result': 'continue',
        'hint': hint,
        'attempts_used': game['attempts'],
        'attempts_remaining': game['max_attempts'] - game['attempts']
    }), 200

@app.route('/game/<game_id>', methods=['GET'])
def get_game_status(game_id):
    """Get current game status"""
    
    if game_id not in games:
        return jsonify({'error': 'Game not found'}), 404
    
    game = games[game_id]
    
    # Don't reveal target number if game is active
    response = {
        'game_id': game['game_id'],
        'player_name': game['player_name'],
        'difficulty': game['difficulty'],
        'status': game['status'],
        'attempts': game['attempts'],
        'max_attempts': game['max_attempts'],
        'guesses': game['guesses']
    }
    
    # Only show target if game is over
    if game['status'] != 'active':
        response['target_number'] = game['target_number']
        response['score'] = game.get('score', 0)
    
    return jsonify(response), 200

@app.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    """Get top 10 players"""
    
    # Sort by score (descending)
    sorted_board = sorted(leaderboard, key=lambda x: x['score'], reverse=True)[:10]
    
    return jsonify({
        'leaderboard': sorted_board,
        'total_games': len(leaderboard)
    }), 200

@app.route('/stats', methods=['GET'])
def get_stats():
    """Get overall game statistics"""
    
    total_games = len(games)
    active_games = len([g for g in games.values() if g['status'] == 'active'])
    won_games = len([g for g in games.values() if g['status'] == 'won'])
    lost_games = len([g for g in games.values() if g['status'] == 'lost'])
    
    return jsonify({
        'total_games': total_games,
        'active_games': active_games,
        'completed_games': won_games + lost_games,
        'won_games': won_games,
        'lost_games': lost_games,
        'win_rate': round(won_games / (won_games + lost_games) * 100, 2) if (won_games + lost_games) > 0 else 0
    }), 200

# Error Handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)