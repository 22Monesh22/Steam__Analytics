# app/utils/dashboard_metadata.py
import json
import os
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class DashboardMetadata:
    def __init__(self):
        self.metadata_cache = {}
        self.dashboard_summaries = self._load_dashboard_summaries()
    
    def _load_dashboard_summaries(self) -> Dict[str, Any]:
        """Load pre-processed dashboard summaries"""
        return {
            "user_analytics": {
                "title": "User Analytics Dashboard",
                "key_metrics": ["Monthly Active Users", "Daily Active Users", "Session Duration", "User Retention", "Geographic Distribution"],
                "main_insights": [
                    "Real-time user engagement tracking across 14M+ Steam users",
                    "Demographic analysis by age, region, and play patterns", 
                    "Retention and churn rate monitoring",
                    "Peak activity time analysis"
                ],
                "data_sources": ["Steam User Database", "Playtime Analytics", "User Profiles"],
                "update_frequency": "15 minutes",
                "primary_charts": ["User Growth Timeline", "Engagement Heatmap", "Retention Funnel", "Geographic Map"]
            },
            "game_analytics": {
                "title": "Game Analytics Dashboard", 
                "key_metrics": ["Total Games", "Average Rating", "Sales Performance", "Genre Popularity", "Price Analysis"],
                "main_insights": [
                    "Analysis of 50,000+ Steam games with performance metrics",
                    "Genre and category performance trends",
                    "Pricing strategy effectiveness",
                    "Release schedule optimization insights"
                ],
                "data_sources": ["Steam Store API", "Sales Database", "Review Analytics"],
                "update_frequency": "30 minutes",
                "primary_charts": ["Sales Trend Analysis", "Rating Distribution", "Genre Performance", "Price vs Rating Scatter"]
            },
            "recommendation_engine": {
                "title": "Recommendation Engine Dashboard",
                "key_metrics": ["Recommendation Accuracy", "Click-Through Rate", "Conversion Rate", "User Engagement", "Personalization Score"],
                "main_insights": [
                    "AI-powered recommendation performance tracking",
                    "User interaction patterns with suggestions",
                    "Personalization effectiveness metrics",
                    "A/B testing results for algorithm improvements"
                ],
                "data_sources": ["Recommendation API", "User Interaction Logs", "A/B Testing Results"],
                "update_frequency": "10 minutes", 
                "primary_charts": ["Accuracy Over Time", "Engagement Funnel", "Personalization Impact", "Algorithm Comparison"]
            }
        }
    
    def get_dashboard_info(self, dashboard_key: str) -> Dict[str, Any]:
        """Get specific dashboard information"""
        return self.dashboard_summaries.get(dashboard_key, {})
    
    def search_metadata(self, query: str, dashboard_key: str = None) -> List[str]:
        """Search for specific information in metadata"""
        # For large files, you'd implement efficient search here
        # This is a simplified version
        results = []
        query = query.lower()
        
        if dashboard_key:
            dashboard_info = self.get_dashboard_info(dashboard_key)
            for key, value in dashboard_info.items():
                if isinstance(value, list):
                    for item in value:
                        if query in str(item).lower():
                            results.append(f"{key}: {item}")
                elif query in str(value).lower():
                    results.append(f"{key}: {value}")
        else:
            # Search across all dashboards
            for dash_key, dash_info in self.dashboard_summaries.items():
                for key, value in dash_info.items():
                    if isinstance(value, list):
                        for item in value:
                            if query in str(item).lower():
                                results.append(f"{dash_key} - {key}: {item}")
                    elif query in str(value).lower():
                        results.append(f"{dash_key} - {key}: {value}")
        
        return results[:10]  # Limit results

# Global instance
dashboard_metadata = DashboardMetadata()