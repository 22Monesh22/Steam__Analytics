import logging
import re
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class DashboardAnalyzer:
    """Analyze queries to identify relevant Power BI dashboards"""
    
    def __init__(self):
        self.dashboards = {
            'sales': {
                'id': 'sales',
                'name': 'Sales Analytics',
                'icon': '💰',
                'keywords': ['sales', 'revenue', 'price', 'cost', 'money', 'profit', 'financial', 'purchase', 'buy']
            },
            'users': {
                'id': 'users', 
                'name': 'User Analytics',
                'icon': '👥',
                'keywords': ['user', 'player', 'customer', 'engagement', 'retention', 'demographic', 'behavior']
            },
            'games': {
                'id': 'games',
                'name': 'Game Analytics', 
                'icon': '🎮',
                'keywords': ['game', 'genre', 'category', 'rating', 'review', 'playtime', 'achievement', 'title']
            },
            'platform': {
                'id': 'platform',
                'name': 'Platform Overview',
                'icon': '📊',
                'keywords': ['platform', 'overview', 'summary', 'dashboard', 'analytics', 'insight', 'trend']
            }
        }
    
    def identify_dashboard(self, query: str) -> List[Dict[str, Any]]:
        """Identify which dashboards are relevant to the query"""
        relevant_dashboards = []
        query_lower = query.lower()
        
        for dash_id, dashboard in self.dashboards.items():
            # Check for keyword matches
            keywords = dashboard['keywords']
            matches = [kw for kw in keywords if kw in query_lower]
            
            if matches:
                dashboard_copy = dashboard.copy()
                dashboard_copy['match_score'] = len(matches)
                dashboard_copy['matched_keywords'] = matches
                relevant_dashboards.append(dashboard_copy)
        
        # Sort by match score and return top 2
        relevant_dashboards.sort(key=lambda x: x['match_score'], reverse=True)
        return relevant_dashboards[:2]
    
    def get_dashboard_suggestions(self, dashboard_ids: List[str]) -> List[str]:
        """Get relevant follow-up questions based on dashboard context"""
        suggestions_map = {
            'sales': [
                "What are the current sales trends?",
                "Which games generate the most revenue?",
                "Show me monthly revenue breakdown",
                "Analyze pricing strategies"
            ],
            'users': [
                "How are user engagement metrics?",
                "What's the user retention rate?",
                "Show me demographic breakdown",
                "Analyze player behavior patterns"
            ],
            'games': [
                "Which genres are most popular?",
                "Show me game rating distribution", 
                "What's the average playtime by category?",
                "Analyze game performance trends"
            ],
            'platform': [
                "Give me platform overview",
                "Show key performance indicators",
                "What are the main trends?",
                "Provide executive summary"
            ]
        }
        
        suggestions = []
        for dash_id in dashboard_ids:
            if dash_id in suggestions_map:
                suggestions.extend(suggestions_map[dash_id])
        
        # Return unique suggestions, max 4
        return list(dict.fromkeys(suggestions))[:4]