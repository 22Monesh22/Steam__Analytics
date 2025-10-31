import os
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class DashboardAIAgent:
    """Unified AI Agent for all dashboard conversations"""
    
    def __init__(self):
        from .conversation_manager import ConversationManager
        from .dashboard_knowledge import DashboardKnowledge
        from ai_engine import AIEngine
        from ai_insights import AIInsights
        
        self.conversation_manager = ConversationManager()
        self.dashboard_knowledge = DashboardKnowledge()
        self.ai_engine = AIEngine()
        self.ai_insights = AIInsights()
        
        logger.info("✅ Dashboard AI Agent initialized successfully")
    
    def process_message(self, user_message, dashboard_url, session_id=None):
        """Main method to process user messages"""
        try:
            # Create session if needed
            if not session_id:
                session_id = self.conversation_manager.create_session()
            
            # Identify dashboard context
            dashboard_id = self.dashboard_knowledge.get_dashboard_by_url(dashboard_url)
            dashboard_info = self.dashboard_knowledge.get_dashboard_info(dashboard_id)
            
            # Add user message to conversation
            self.conversation_manager.add_message(
                session_id, 'user', user_message, dashboard_id
            )
            
            # Get conversation context
            conversation_context = self.conversation_manager.get_conversation_context(session_id)
            
            # Generate AI response
            ai_response = self._generate_ai_response(
                user_message, dashboard_info, conversation_context
            )
            
            # Add AI response to conversation
            self.conversation_manager.add_message(
                session_id, 'assistant', ai_response['response'], dashboard_id
            )
            
            # Prepare final response
            response_data = {
                'success': True,
                'response': ai_response['response'],
                'suggestions': ai_response.get('suggestions', []),
                'session_id': session_id,
                'dashboard_context': dashboard_id,
                'timestamp': datetime.now().isoformat()
            }
            
            logger.info(f"✅ AI response generated for dashboard: {dashboard_id}")
            return response_data
            
        except Exception as e:
            logger.error(f"❌ Error in AI agent: {str(e)}")
            return {
                'success': False,
                'response': "I apologize, but I'm having trouble processing your request right now. Please try again in a moment.",
                'suggestions': ["Try rephrasing your question", "Ask about dashboard metrics", "Request an explanation"],
                'session_id': session_id or 'error',
                'error': str(e)
            }
    
    def _generate_ai_response(self, user_message, dashboard_info, conversation_context):
        """Generate intelligent response using available AI engines"""
        try:
            # Build enhanced prompt
            prompt = self._build_enhanced_prompt(user_message, dashboard_info, conversation_context)
            
            # Try Gemini API first
            try:
                # Use your existing AI engine
                data_context = {
                    'dashboard': dashboard_info['name'],
                    'metrics': dashboard_info['key_metrics'],
                    'user_query': user_message
                }
                
                insight = self.ai_engine.generate_insight(data_context, 'steam_specific')
                
                # Enhance with AI insights
                enhanced_response = self._enhance_response(insight, user_message, dashboard_info)
                
                # Generate follow-up suggestions
                suggestions = self.conversation_manager.generate_follow_ups(user_message, dashboard_info['name'])
                
                return {
                    'response': enhanced_response,
                    'suggestions': suggestions[:3] + dashboard_info['common_questions'][:3]
                }
                
            except Exception as e:
                logger.warning(f"Gemini API failed, using fallback: {e}")
                # Fallback to simple responses
                return self._generate_fallback_response(user_message, dashboard_info)
                
        except Exception as e:
            logger.error(f"Error in response generation: {e}")
            return {
                'response': f"I'm here to help with the {dashboard_info['name']}. This dashboard focuses on {dashboard_info['description']}. What would you like to know?",
                'suggestions': dashboard_info['common_questions'][:4]
            }
    
    def _build_enhanced_prompt(self, user_message, dashboard_info, conversation_context):
        """Build comprehensive prompt for AI"""
        prompt = f"""
        DASHBOARD CONTEXT:
        - Dashboard: {dashboard_info['name']}
        - Description: {dashboard_info['description']}
        - Key Metrics: {', '.join(dashboard_info['key_metrics'])}
        
        CONVERSATION HISTORY:
        {conversation_context}
        
        USER QUESTION: {user_message}
        
        REQUIREMENTS:
        1. Provide specific, actionable insights about this dashboard
        2. Reference actual metrics and data patterns
        3. Maintain conversational, helpful tone
        4. Suggest relevant follow-up questions
        5. Focus on practical business insights
        
        RESPONSE FORMAT:
        - Start with direct answer
        - Provide 2-3 key points
        - End with helpful suggestions
        """
        return prompt
    
    def _enhance_response(self, base_response, user_message, dashboard_info):
        """Enhance AI response with context"""
        enhanced = f"**{dashboard_info['name']} Analysis**\n\n"
        enhanced += base_response + "\n\n"
        enhanced += f"💡 *This insight is based on {dashboard_info['description'].lower()}*"
        return enhanced
    
    def _generate_fallback_response(self, user_message, dashboard_info):
        """Generate fallback response when AI fails"""
        responses = {
            'user_analytics': [
                f"Based on User Analytics data: {user_message}. Key metrics include {', '.join(dashboard_info['key_metrics'][:3])}.",
                f"User Analytics shows: {user_message}. Focus areas are engagement and retention patterns.",
                f"For User Analytics: {user_message}. I can help explain user behavior metrics."
            ],
            'game_analytics': [
                f"Game Analytics indicates: {user_message}. Tracking {', '.join(dashboard_info['key_metrics'][:3])}.",
                f"Regarding game performance: {user_message}. Key metrics include sales and ratings.",
                f"From Game Analytics: {user_message}. I can analyze game trends and performance."
            ],
            'recommendation_engine': [
                f"Recommendation Engine data shows: {user_message}. Monitoring {', '.join(dashboard_info['key_metrics'][:3])}.",
                f"For recommendations: {user_message}. Focused on accuracy and user engagement.",
                f"Recommendation insights: {user_message}. I can explain AI suggestion patterns."
            ]
        }
        
        dashboard_id = self.dashboard_knowledge.get_dashboard_by_url('')
        fallback_responses = responses.get(dashboard_id, responses['user_analytics'])
        
        import random
        return {
            'response': random.choice(fallback_responses),
            'suggestions': dashboard_info['common_questions'][:4]
        }