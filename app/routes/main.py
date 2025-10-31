from flask import Blueprint, render_template, jsonify
import json
import os

main_bp = Blueprint('main', __name__)

# Sample data for demonstration
SAMPLE_GAMES = [
    {"id": 1, "name": "Counter-Strike 2", "players": 1250000, "rating": 88, "genre": "FPS"},
    {"id": 2, "name": "Dota 2", "players": 800000, "rating": 90, "genre": "MOBA"},
    {"id": 3, "name": "PUBG: Battlegrounds", "players": 600000, "rating": 86, "genre": "Battle Royale"},
    {"id": 4, "name": "Apex Legends", "players": 450000, "rating": 87, "genre": "Battle Royale"},
    {"id": 5, "name": "Grand Theft Auto V", "players": 200000, "rating": 92, "genre": "Action"},
]

SAMPLE_USERS = [
    {"id": 1, "name": "Gamer_Pro", "preferences": ["FPS", "Action"], "cluster": "Competitive"},
    {"id": 2, "name": "Casual_Player", "preferences": ["RPG", "Adventure"], "cluster": "Casual"},
    {"id": 3, "name": "Strategy_Fan", "preferences": ["Strategy", "Simulation"], "cluster": "Strategic"},
]

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/api/games')
def get_games():
    return jsonify({"games": SAMPLE_GAMES})

@main_bp.route('/api/users')
def get_users():
    return jsonify({"users": SAMPLE_USERS})

@main_bp.route('/api/analytics/trends')
def get_trends():
    trends = [
        {"period": "Jan", "players": 1000000, "recommendations": 50000},
        {"period": "Feb", "players": 1200000, "recommendations": 60000},
        {"period": "Mar", "players": 1100000, "recommendations": 55000},
        {"period": "Apr", "players": 1300000, "recommendations": 70000},
        {"period": "May", "players": 1400000, "recommendations": 75000},
    ]
    return jsonify({"trends": trends})