# tests/test_validation.py
"""Tests for input validation"""

from typing import Literal
import pytest

class TestGuessValidation:
    """Test suite for guess validation"""
    
    def test_guess_non_integer_returns_400(self, client, sample_game):
        """Test non-integer guess is rejected"""
        response = client.post(f'/game/{sample_game}/guess', json={
            'guess': 'abc'
        })
        assert response.status_code == 400
    
    def test_guess_negative_number_rejected(self, client, sample_game):
        """Test negative numbers are rejected"""
        response = client.post(f'/game/{sample_game}/guess', json={
            'guess': -5
        })
        assert response.status_code == 400
    
    def test_guess_zero_rejected(self, client, sample_game):
        """Test zero is rejected (out of range)"""
        response = client.post(f'/game/{sample_game}/guess', json={
            'guess': 0
        })
        assert response.status_code == 400
    
    def test_guess_above_range_easy(self, client):
        """Test guess above easy mode range (1-50)"""
        response = client.post('/game/start', json={
            'player_name': 'TestHero',
            'difficulty': 'easy'
        })
        game_id = response.get_json()['game_id']
        
        response = client.post(f'/game/{game_id}/guess', json={
            'guess': 100
        })
        assert response.status_code == 400
        data = response.get_json()
        assert 'between' in data['error'].lower()
    
    def test_guess_below_range(self, client, sample_game):
        """Test guess below minimum range"""
        response = client.post(f'/game/{sample_game}/guess', json={
            'guess': -10
        })
        assert response.status_code == 400
    
    def test_guess_decimal_number(self, client, sample_game):
        """Test decimal number handling"""
        response = client.post(f'/game/{sample_game}/guess', json={
            'guess': 25.5
        })
        # Document behavior - does it round or reject?
        if response.status_code == 200:
            print("ℹ️ Decimal numbers are accepted (rounded)")
        elif response.status_code == 400:
            print("✅ Decimal numbers are properly rejected")
    
    def test_guess_very_large_number(self, client, sample_game):
        """Test extremely large number"""
        response = client.post(f'/game/{sample_game}/guess', json={
            'guess': 999999999
        })
        assert response.status_code == 400
    
    def test_guess_float_as_string(self, client, sample_game):
        """Test float as string"""
        response = client.post(f'/game/{sample_game}/guess', json={
            'guess': "25.7"
        })
        # Should be rejected as non-integer
        assert response.status_code == 400
    
    def test_guess_null_value(self, client, sample_game):
        """Test null/None guess value"""
        response = client.post(f'/game/{sample_game}/guess', json={
            'guess': None
        })
        assert response.status_code == 400
    
    def test_guess_missing_field(self, client, sample_game):
        """Test request without guess field"""
        response = client.post(f'/game/{sample_game}/guess', json={})
        assert response.status_code == 400
    
    def test_guess_empty_json(self, client, sample_game):
        """Test request with no JSON body"""
        response = client.post(f'/game/{sample_game}/guess')
        assert response.status_code in [400, 415]

class TestRangeValidation:
    """Test range validation for different difficulties"""
    
    @pytest.mark.parametrize("difficulty,min_val,max_val", [
        ('easy', 1, 50),
        ('medium', 1, 100),
        ('hard', 1, 200)
    ])
    def test_valid_range_accepted(self, client, difficulty: Literal['easy'] | Literal['medium'] | Literal['hard'], min_val: Literal[1], max_val: Literal[50] | Literal[100] | Literal[200]):
        """Test valid guesses within range are accepted"""
        response = client.post('/game/start', json={
            'player_name': 'TestHero',
            'difficulty': difficulty
        })
        game_id = response.get_json()['game_id']
        
        # Test minimum value
        response = client.post(f'/game/{game_id}/guess', json={
            'guess': min_val
        })
        assert response.status_code == 200
        
        # Start new game for max value test
        response = client.post('/game/start', json={
            'player_name': 'TestHero',
            'difficulty': difficulty
        })
        game_id = response.get_json()['game_id']
        
        # Test maximum value
        response = client.post(f'/game/{game_id}/guess', json={
            'guess': max_val
        })
        assert response.status_code == 200
    
    @pytest.mark.parametrize("difficulty,invalid_guess", [
        ('easy', 51),
        ('easy', 100),
        ('medium', 101),
        ('medium', 200),
        ('hard', 201),
        ('hard', 300)
    ])
    def test_out_of_range_rejected(self, client, difficulty: Literal['easy'] | Literal['medium'] | Literal['hard'], invalid_guess: Literal[51] | Literal[100] | Literal[101] | Literal[200] | Literal[201] | Literal[300]):
        """Test guesses outside range are rejected"""
        response = client.post('/game/start', json={
            'player_name': 'TestHero',
            'difficulty': difficulty
        })
        game_id = response.get_json()['game_id']
        
        response = client.post(f'/game/{game_id}/guess', json={
            'guess': invalid_guess
        })
        assert response.status_code == 400