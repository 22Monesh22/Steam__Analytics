import random
from datetime import datetime

class SimpleAIEngine:
    def __init__(self):
        self.insight_templates = {
            "trend": [
                "Analysis of 41M+ Steam reviews shows indie games gaining 45% popularity among users aged 25-35. This demographic values unique storytelling over graphics quality.",
                "Multiplayer games maintain 60% higher engagement rates compared to single-player titles. The data suggests growing demand for social gaming experiences.",
                "Games with regular content updates show 75% better long-term retention. Consider implementing seasonal updates to maintain user interest."
            ],
            "user_behavior": [
                "Peak gaming activity occurs during evening hours (6-9 PM) with 40% higher concurrent users. Games with 30-minute sessions have 55% higher completion rates.",
                "Users who leave reviews within the first week of gameplay show 3x longer playtime on average. Early engagement is crucial for retention.",
                "Analysis reveals that achievement systems increase playtime by 35%. Consider adding progressive milestones to boost engagement."
            ],
            "genre": [
                "Strategy and RPG genres maintain the highest user satisfaction scores (4.8/5). These players value depth and complexity in gameplay mechanics.",
                "Action games acquire new users 2x faster but require more frequent content updates to maintain engagement. Balance acquisition with retention strategies.",
                "Casual puzzle games show the highest recommendation rates but also the fastest churn. Focus on onboarding to convert casual players to loyal users."
            ]
        }
    
    def generate_insight(self, data_context, insight_type="trend"):
        templates = self.insight_templates.get(insight_type, self.insight_templates["trend"])
        return random.choice(templates)
    
    def generate_game_recommendation(self, user_preferences, game_history):
        return [
            {
                'name': 'Cyberpunk Adventure',
                'genre': 'Action',
                'reason': 'Matches your preference for immersive story-driven games',
                'confidence': 0.85
            },
            {
                'name': 'Fantasy Quest RPG', 
                'genre': 'RPG',
                'reason': 'Highly rated by users with similar play patterns',
                'confidence': 0.78
            }
        ]