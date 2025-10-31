class DashboardKnowledge:
    """Knowledge base for all Power BI dashboards"""
    
    def __init__(self):
        self.dashboards = {
            'user_analytics': {
                'name': 'User Analytics Dashboard',
                'description': 'User behavior, engagement metrics, and retention analysis',
                'key_metrics': ['Daily Active Users (DAU)', 'Monthly Active Users (MAU)', 'Retention Rate', 'Session Duration', 'User Clusters'],
                'common_questions': [
                    "How are users engaging with our platform?",
                    "What are the peak usage hours?",
                    "Show me user retention trends",
                    "Explain the user segmentation",
                    "What's the DAU/MAU ratio?"
                ],
                'focus_areas': ['user behavior', 'engagement', 'demographics', 'retention']
            },
            'game_analytics': {
                'name': 'Game Analytics Dashboard', 
                'description': 'Game performance, sales trends, ratings, and genre analysis',
                'key_metrics': ['Total Sales', 'Average Rating', 'Genre Distribution', 'Review Count', 'Price Points'],
                'common_questions': [
                    "Which games are performing best?",
                    "Show sales trends by genre",
                    "What's the rating distribution?",
                    "Compare game performance",
                    "What genres are most popular?"
                ],
                'focus_areas': ['game performance', 'sales', 'ratings', 'genres']
            },
            'recommendation_engine': {
                'name': 'Recommendation Engine Dashboard',
                'description': 'AI recommendation performance and accuracy metrics',
                'key_metrics': ['Click-Through Rate (CTR)', 'Conversion Rate', 'Accuracy Score', 'User Satisfaction', 'Recommendation Diversity'],
                'common_questions': [
                    "How accurate are our recommendations?",
                    "What factors influence suggestions?",
                    "Show recommendation performance",
                    "Explain the algorithm metrics",
                    "How can we improve suggestions?"
                ],
                'focus_areas': ['recommendations', 'AI accuracy', 'user preferences', 'suggestions']
            }
        }
    
    def get_dashboard_by_url(self, url):
        """Identify dashboard from URL"""
        if 'user-analytics' in url.lower():
            return 'user_analytics'
        elif 'game-analytics' in url.lower():
            return 'game_analytics'
        elif 'recommendation' in url.lower():
            return 'recommendation_engine'
        return 'user_analytics'  # default
    
    def get_dashboard_info(self, dashboard_id):
        """Get complete dashboard information"""
        return self.dashboards.get(dashboard_id, self.dashboards['user_analytics'])
    
    def get_suggestions(self, dashboard_id):
        """Get suggested questions for dashboard"""
        info = self.get_dashboard_info(dashboard_id)
        return info['common_questions'][:6]