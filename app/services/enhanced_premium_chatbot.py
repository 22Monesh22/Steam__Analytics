# app/services/enhanced_premium_chatbot.py
import logging
import random
from typing import Dict, Any, List
from app.services.powerbi_data_fetcher import PowerBIDataFetcher

logger = logging.getLogger(__name__)

class EnhancedPremiumChatbot:
    def __init__(self):
        self.data_fetcher = PowerBIDataFetcher()
        self.conversation_context = {}
        
    async def process_message(self, user_message: str, user_context: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """Process user message with enhanced Power BI integration"""
        try:
            # Analyze message intent
            intent_analysis = self._analyze_message_intent(user_message)
            dashboard_type = intent_analysis['dashboard_type']
            
            # Fetch real-time data from Power BI
            powerbi_data = await self.data_fetcher.fetch_dashboard_insights(dashboard_type)
            
            # Generate contextual response
            response = await self._generate_contextual_response(
                user_message, intent_analysis, powerbi_data, user_context
            )
            
            return {
                'success': True,
                'response': response['text'],
                'suggestions': response['suggestions'],
                'data_insights': response['data_insights'],
                'visualization_hint': response.get('visualization_hint'),
                'emotional_context': response['emotional_context'],
                'session_id': session_id,
                'is_premium': True
            }
            
        except Exception as e:
            logger.error(f"Enhanced chatbot error: {e}")
            return self._get_error_response(session_id)
    
    def _analyze_message_intent(self, message: str) -> Dict[str, Any]:
        """Analyze user message to determine intent and context"""
        message_lower = message.lower()
        
        # Determine dashboard type
        if any(word in message_lower for word in ['user', 'player', 'engagement', 'retention']):
            dashboard_type = "user_analytics"
        elif any(word in message_lower for word in ['game', 'sales', 'rating', 'genre']):
            dashboard_type = "game_analytics"
        elif any(word in message_lower for word in ['recommendation', 'suggestion', 'ai', 'algorithm']):
            dashboard_type = "recommendation_engine"
        else:
            dashboard_type = "user_analytics"  # default
        
        # Determine query type
        if any(word in message_lower for word in ['trend', 'change', 'growth', 'over time']):
            query_type = "trend"
        elif any(word in message_lower for word in ['current', 'now', 'latest', 'real-time']):
            query_type = "current"
        elif any(word in message_lower for word in ['compare', 'vs', 'versus', 'difference']):
            query_type = "comparison"
        elif any(word in message_lower for word in ['insight', 'analysis', 'understand']):
            query_type = "insight"
        else:
            query_type = "general"
        
        return {
            'dashboard_type': dashboard_type,
            'query_type': query_type,
            'needs_metrics': any(word in message_lower for word in ['metric', 'number', 'stat', 'data']),
            'needs_insights': any(word in message_lower for word in ['insight', 'analysis', 'trend']),
            'emotional_tone': self._detect_emotional_tone(message)
        }
    
    async def _generate_contextual_response(self, user_message: str, intent_analysis: Dict, 
                                          powerbi_data: Dict, user_context: Dict) -> Dict[str, Any]:
        """Generate contextual response with Power BI data"""
        dashboard_type = intent_analysis['dashboard_type']
        query_type = intent_analysis['query_type']
        
        # Base response template
        response = {
            'text': "",
            'suggestions': [],
            'data_insights': [],
            'emotional_context': intent_analysis['emotional_tone']
        }
        
        # Add emotional opening based on tone
        emotional_openings = {
            'analytical': "🔍 Based on the latest Power BI analytics...",
            'curious': "💡 That's an excellent question! Here's what the data shows...",
            'professional': "📊 According to our real-time dashboard metrics...",
            'enthusiastic': "🎯 Great question! Let me share some exciting insights..."
        }
        
        opening = emotional_openings.get(intent_analysis['emotional_tone'], "📈 Here's the latest from our analytics...")
        response['text'] += opening + "\n\n"
        
        # Add metrics if requested
        if intent_analysis['needs_metrics'] and powerbi_data.get('metrics'):
            response['text'] += "**Key Metrics:**\n"
            for metric_name, metric_data in powerbi_data['metrics'].items():
                trend_emoji = "📈" if metric_data.get('trend') == 'up' else "📉" if metric_data.get('trend') == 'down' else "➡️"
                change_text = f" ({trend_emoji} {metric_data.get('change', 0)}%)" if metric_data.get('change') else ""
                response['text'] += f"• **{self._format_metric_name(metric_name)}**: {metric_data['value']}{change_text}\n"
            response['text'] += "\n"
        
        # Add insights
        if powerbi_data.get('insights'):
            response['text'] += "**Latest Insights:**\n"
            for insight in powerbi_data['insights']:
                response['text'] += f"• {insight}\n"
            response['data_insights'] = powerbi_data['insights']
        
        # Add contextual suggestions
        response['suggestions'] = self._generate_contextual_suggestions(dashboard_type, query_type)
        
        # Add visualization hint for complex data
        if intent_analysis['query_type'] in ['trend', 'comparison']:
            response['visualization_hint'] = f"Would you like me to create a visual trend analysis for this {dashboard_type.replace('_', ' ')} data?"
        
        return response
    
    def _detect_emotional_tone(self, message: str) -> str:
        """Detect emotional tone of the message"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['!', 'amazing', 'wow', 'great', 'excellent']):
            return 'enthusiastic'
        elif any(word in message_lower for word in ['?', 'how', 'what', 'why', 'explain']):
            return 'curious'
        elif any(word in message_lower for word in ['analyze', 'data', 'metrics', 'numbers']):
            return 'analytical'
        else:
            return 'professional'
    
    def _format_metric_name(self, metric_name: str) -> str:
        """Format metric names for better readability"""
        name_map = {
            'monthly_active_users': 'Monthly Active Users',
            'daily_active_users': 'Daily Active Users',
            'avg_session_duration': 'Avg Session Duration',
            'retention_rate': 'Retention Rate',
            'total_games': 'Total Games',
            'average_rating': 'Average Rating',
            'recommendation_accuracy': 'Recommendation Accuracy',
            'click_through_rate': 'Click-Through Rate'
        }
        return name_map.get(metric_name, metric_name.replace('_', ' ').title())
    
    def _generate_contextual_suggestions(self, dashboard_type: str, query_type: str) -> List[str]:
        """Generate contextual suggestions based on dashboard and query type"""
        suggestions_map = {
            'user_analytics': {
                'trend': ["Show user growth trends", "Engagement patterns over time", "Retention rate history"],
                'current': ["Current active users", "Real-time engagement metrics", "Latest retention stats"],
                'comparison': ["Compare user segments", "Platform engagement comparison", "Geographic performance"],
                'general': ["User behavior analysis", "Demographic insights", "Engagement optimization tips"]
            },
            'game_analytics': {
                'trend': ["Sales trends analysis", "Rating changes over time", "Genre popularity evolution"],
                'current': ["Latest game performance", "Current top sellers", "Real-time review sentiment"],
                'comparison': ["Compare game genres", "Price performance analysis", "Platform comparison"],
                'general': ["Market trends", "Pricing insights", "Release strategy analysis"]
            },
            'recommendation_engine': {
                'trend': ["Accuracy improvement timeline", "Engagement growth trends", "Algorithm performance history"],
                'current': ["Current recommendation stats", "Real-time user engagement", "Latest A/B test results"],
                'comparison': ["Compare algorithms", "User segment performance", "Platform effectiveness"],
                'general': ["Personalization insights", "Engagement optimization", "Algorithm improvements"]
            }
        }
        
        return suggestions_map.get(dashboard_type, {}).get(query_type, [
            "Explain key metrics",
            "Show recent trends", 
            "Provide detailed analysis"
        ])
    
    def _get_error_response(self, session_id: str) -> Dict[str, Any]:
        """Get error response when something goes wrong"""
        return {
            'success': False,
            'response': "🌟 I appreciate your question! I'm currently enhancing my data connectivity to provide you with the most accurate Power BI insights. Let me share some general analytics knowledge while I work on the real-time connection!",
            'suggestions': [
                "Ask about user analytics trends",
                "Explore game performance metrics",
                "Get recommendation engine insights"
            ],
            'session_id': session_id,
            'is_premium': True,
            'emotional_intelligence': True
        }