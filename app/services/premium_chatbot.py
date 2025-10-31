import logging
from typing import Dict, List, Any
from datetime import datetime
from app.services.emotional_ai_engine import EmotionalAIEngine
import json
import uuid

logger = logging.getLogger(__name__)

class PremiumChatbot:
    """Premium chatbot with emotional intelligence and multi-domain expertise"""
    
    def __init__(self):
        self.ai_engine = EmotionalAIEngine()
        self.conversation_memory = {}
        
    def process_message(self, user_message: str, user_context: Dict, session_id: str) -> Dict[str, Any]:
        """Process user message with emotional intelligence and context awareness"""
        try:
            # Initialize or update conversation memory
            if session_id not in self.conversation_memory:
                self.conversation_memory[session_id] = {
                    'history': [],
                    'user_preferences': {},
                    'last_interaction': datetime.now(),
                    'conversation_topics': set(),
                    'emotional_patterns': [],
                    'interaction_count': 0
                }
            
            memory = self.conversation_memory[session_id]
            memory['interaction_count'] += 1
            
            # Add user message to history
            memory['history'].append({
                'role': 'user',
                'content': user_message,
                'timestamp': datetime.now().isoformat(),
                'emotional_tone': self.ai_engine.analyze_emotion(user_message)
            })
            
            # Analyze conversation context
            context_analysis = self._analyze_conversation_context(user_message, memory)
            
            # Determine optimal response style
            response_style = self.ai_engine.get_conversation_style(user_message)
            
            # Generate premium AI response
            ai_response = self.ai_engine.generate_chat_response(
                user_message, 
                memory['history'],
                style=response_style
            )
            
            # Add AI response to memory
            memory['history'].append({
                'role': 'assistant',
                'content': ai_response,
                'timestamp': datetime.now().isoformat(),
                'response_style': response_style
            })
            
            # Update emotional patterns
            memory['emotional_patterns'].append(context_analysis['emotion_analysis'])
            
            # Keep history manageable (last 15 exchanges)
            if len(memory['history']) > 30:
                memory['history'] = memory['history'][-20:]
            
            # Generate intelligent contextual suggestions
            suggestions = self._generate_premium_suggestions(user_message, context_analysis, memory)
            
            # Build premium response
            premium_response = {
                'success': True,
                'response': ai_response,
                'suggestions': suggestions,
                'response_style': response_style,
                'context_analysis': context_analysis,
                'is_premium': True,
                'timestamp': datetime.now().isoformat(),
                'conversation_depth': len(memory['history']) // 2,
                'emotional_intelligence': True,
                'session_id': session_id,
                'interaction_count': memory['interaction_count']
            }
            
            return premium_response
            
        except Exception as e:
            logger.error(f"Premium chatbot error: {e}")
            return self._create_premium_error_response(user_message, session_id)
    
    def _analyze_conversation_context(self, user_message: str, memory: Dict) -> Dict[str, Any]:
        """Advanced conversation context analysis"""
        message_lower = user_message.lower()
        
        # Emotional analysis
        emotion_analysis = self.ai_engine.analyze_emotion(user_message)
        
        # Topic detection with weights
        topics = set()
        topic_keywords = {
            'steam_analytics': ['steam', 'game', 'analytics', 'data', 'metric', 'user', 'sales', 'revenue', 'player'],
            'technology': ['technical', 'code', 'api', 'integration', 'system', 'architecture', 'software', 'development'],
            'business': ['business', 'strategy', 'revenue', 'growth', 'market', 'competitor', 'monetization', 'profit'],
            'creative': ['creative', 'idea', 'innovative', 'brainstorm', 'design', 'art', 'story', 'narrative'],
            'personal': ['you', 'your', 'how are', 'feeling', 'emotion', 'personal', 'about you'],
            'general_knowledge': ['weather', 'news', 'world', 'politics', 'science', 'history'],
            'entertainment': ['movie', 'music', 'book', 'entertainment', 'fun', 'hobby'],
            'education': ['learn', 'study', 'education', 'teach', 'explain', 'understand']
        }
        
        for topic, keywords in topic_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                topics.add(topic)
                memory['conversation_topics'].add(topic)
        
        # Intent analysis
        intent = 'general_inquiry'
        if any(word in message_lower for word in ['how', 'why', 'explain', 'clarify']):
            intent = 'explanation'
        elif any(word in message_lower for word in ['analyze', 'data', 'metric', 'statistic']):
            intent = 'analysis'
        elif any(word in message_lower for word in ['help', 'support', 'problem', 'issue']):
            intent = 'support'
        elif any(word in message_lower for word in ['idea', 'suggest', 'recommend', 'advice']):
            intent = 'recommendation'
        elif any(word in message_lower for word in ['create', 'build', 'make', 'develop']):
            intent = 'creation'
        elif any(word in message_lower for word in ['compare', 'versus', 'vs', 'difference']):
            intent = 'comparison'
        
        return {
            'topics': list(topics),
            'intent': intent,
            'emotion_analysis': emotion_analysis,
            'requires_data': any(word in message_lower for word in ['number', 'data', 'metric', 'statistic', 'percentage']),
            'is_complex': len(user_message.split()) > 12,
            'requires_creativity': any(word in message_lower for word in ['creative', 'innovative', 'idea', 'brainstorm']),
            'is_personal': any(word in message_lower for word in ['you', 'your', 'personal', 'feel'])
        }
    
    def _generate_premium_suggestions(self, user_message: str, context: Dict, memory: Dict) -> List[str]:
        """Generate intelligent, contextual follow-up suggestions"""
        
        base_suggestions = [
            "Tell me more about your thoughts on this",
            "Can you provide specific examples?",
            "How would you apply this in practice?",
            "What are the broader implications?"
        ]
        
        contextual_suggestions = []
        
        # Topic-based premium suggestions
        topic_suggestions = {
            'steam_analytics': [
                "Analyze recent gaming market trends",
                "Explore user engagement patterns in detail",
                "Compare performance across different genres",
                "Predict future gaming industry developments"
            ],
            'technology': [
                "Discuss the latest tech innovations",
                "Explore technical implementation strategies",
                "Compare different technology approaches",
                "Review scalability and performance considerations"
            ],
            'business': [
                "Develop comprehensive business strategies",
                "Analyze market opportunities in depth",
                "Optimize revenue and growth strategies",
                "Conduct competitive landscape analysis"
            ],
            'creative': [
                "Brainstorm innovative solutions together",
                "Explore creative possibilities and ideas",
                "Develop unique design approaches",
                "Create compelling narratives and stories"
            ],
            'personal': [
                "Share more about your perspective",
                "Discuss personal growth and development",
                "Explore emotional intelligence topics",
                "Build our conversational relationship"
            ]
        }
        
        # Add topic-specific suggestions
        for topic in context['topics']:
            if topic in topic_suggestions:
                contextual_suggestions.extend(topic_suggestions[topic])
        
        # Intent-based suggestions
        if context['intent'] == 'analysis':
            contextual_suggestions.extend([
                "Provide deeper data analysis",
                "Explore alternative analytical approaches",
                "Compare with industry benchmarks",
                "Identify key performance indicators"
            ])
        elif context['intent'] == 'creative':
            contextual_suggestions.extend([
                "Generate more creative ideas",
                "Explore different creative angles",
                "Develop implementation plans",
                "Brainstorm innovative features"
            ])
        
        # Emotional context suggestions
        if context['emotion_analysis']['primary_emotion'] == 'confused':
            contextual_suggestions.extend([
                "Break this down into simpler concepts",
                "Provide step-by-step explanation",
                "Share relevant examples and analogies",
                "Clarify any remaining uncertainties"
            ])
        elif context['emotion_analysis']['primary_emotion'] == 'curious':
            contextual_suggestions.extend([
                "Explore this topic in more depth",
                "Discuss related concepts and ideas",
                "Share interesting facts and insights",
                "Connect this to broader knowledge areas"
            ])
        
        # Mix and deduplicate suggestions
        all_suggestions = contextual_suggestions + base_suggestions
        unique_suggestions = list(dict.fromkeys(all_suggestions))
        
        return unique_suggestions[:6]  # Return top 6 premium suggestions
    
    def _create_premium_error_response(self, user_message: str, session_id: str) -> Dict[str, Any]:
        """Create elegant premium error response"""
        emotion_analysis = self.ai_engine.analyze_emotion(user_message)
        
        return {
            'success': False,
            'response': f"🌟 I appreciate your message about '{user_message}'. I'm currently optimizing my premium response capabilities to provide you with even more valuable insights. Let's continue our conversation with renewed energy! 💫",
            'suggestions': [
                "Let's try a different approach",
                "Ask me about advanced analytics",
                "Discuss innovative ideas",
                "Explore emotional intelligence topics",
                "Share your thoughts on technology",
                "Let's brainstorm creative solutions"
            ],
            'is_premium': True,
            'emotional_intelligence': True,
            'timestamp': datetime.now().isoformat(),
            'session_id': session_id
        }
    
    def get_premium_welcome(self, user_context: Dict) -> Dict[str, Any]:
        """Get premium welcome message with emotional intelligence"""
        session_id = str(uuid.uuid4())
        
        return {
            'success': True,
            'response': """🌟 **Welcome to Premium Emotional AI Assistant!**

I'm your advanced AI companion with **exceptional emotional intelligence** and **multi-domain expertise**. Here's what makes our conversation special:

🎯 **Advanced Capabilities:**
• **Emotional Intelligence**: I understand and respond to your emotional state
• **Multi-Domain Mastery**: Technology, Business, Psychology, Gaming, Creativity & more
• **Contextual Awareness**: I remember our conversation flow and adapt accordingly
• **Creative Problem Solving**: Innovative solutions and unique perspectives

💡 **What I Can Help With:**
• Deep gaming analytics & market insights
• Technology trends & innovation discussions
• Business strategy & growth planning
• Creative brainstorming & idea generation
• Personal development & emotional intelligence
• And much more across various domains!

🚀 **Premium Features:**
• Emotional context adaptation
• Intelligent conversation memory
• Multi-topic expertise
• Creative and analytical thinking
• Personalized interaction style

**I'm here to understand you, adapt to your needs, and provide genuinely valuable insights across any topic!**

What would you like to explore together today?""",
            'suggestions': [
                "Analyze current gaming industry trends",
                "Discuss emotional intelligence in AI",
                "Explore technology innovations",
                "Help with business strategy development",
                "Brainstorm creative ideas together",
                "Have a meaningful conversation about life"
            ],
            'is_premium': True,
            'emotional_intelligence': True,
            'timestamp': datetime.now().isoformat(),
            'session_id': session_id,
            'welcome_style': 'premium'
        }