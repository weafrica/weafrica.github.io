from flask import Blueprint, render_template, request, redirect, url_for, session
from functools import wraps
import game  # Import the game module

game_bp = Blueprint('game', __name__)

@game_bp.route('/game')
def game_list():
    # Fetch all games from the database
    games = game.get_all_games()
    return render_template('game_list.html', games=games)

@game_bp.route('/game_detail/<int:game_id>')
def game_detail(game_id):
    # Fetch the game from the database
    game_detail = game.get_game(game_id)
    return render_template('game_detail.html', game=game_detail)