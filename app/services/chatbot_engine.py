import logging
from typing import Dict, List, Any
from datetime import datetime
from app.services.ai_engine import AIEngine
from app.services.dashboard_analyzer import DashboardAnalyzer

logger = logging.getLogger(__name__)

class UnlimitedChatbotEngine:
    """Unbounded chatbot that can think beyond the application"""
    
    def __init__(self):
        self.ai_engine = AIEngine()
        self.dashboard_analyzer = DashboardAnalyzer()
        
        # Beyond-thinking domains
        self.expanded_domains = {
            'industry_analysis': [
                'gaming industry', 'market trends', 'competitors', 'industry news',
                'emerging technologies', 'market analysis', 'business strategy'
            ],
            'technical_innovation': [
                'ai in gaming', 'new technologies', 'technical architecture',
                'software development', 'data science', 'machine learning'
            ],
            'user_experience': [
                'ui/ux design', 'user psychology', 'customer journey',
                'interface design', 'user testing', 'accessibility'
            ],
            'business_growth': [
                'monetization', 'business models', 'growth strategies',
                'partnerships', 'marketing', 'customer acquisition'
            ],
            'future_trends': [
                'future predictions', 'emerging trends', 'innovation opportunities',
                'market disruptions', 'technology evolution'
            ],
            'general_knowledge': [
                'general questions', 'conceptual discussions', 'creative ideas',
                'philosophical questions', 'career advice'
            ]
        }
    
    def process_query(self, user_query: str, user_context: Dict = None) -> Dict[str, Any]:
        """Process ANY type of query - with expanded thinking capabilities"""
        try:
            # Analyze if query goes beyond application scope
            query_scope = self._analyze_query_scope(user_query)
            
            if query_scope['is_beyond_application']:
                return self._handle_beyond_thinking(user_query, query_scope, user_context)
            else:
                return self._handle_standard_query(user_query, user_context)
                
        except Exception as e:
            logger.error(f"Unlimited chatbot error: {e}")
            return self._create_error_response()

    def _analyze_query_scope(self, query: str) -> Dict[str, Any]:
        """Analyze how far beyond the application the query goes"""
        query_lower = query.lower()
        
        # Check for Steam/application specific terms
        steam_terms = ['steam', 'dashboard', 'powerbi', 'sales', 'revenue', 'user analytics', 'game data']
        is_steam_related = any(term in query_lower for term in steam_terms)
        
        # Check for beyond-thinking domains
        beyond_domains = []
        for domain, keywords in self.expanded_domains.items():
            if any(keyword in query_lower for keyword in keywords):
                beyond_domains.append(domain)
        
        return {
            'is_beyond_application': len(beyond_domains) > 0 or not is_steam_related,
            'beyond_domains': beyond_domains,
            'is_steam_related': is_steam_related,
            'complexity_level': self._assess_complexity(query)
        }

    def _handle_beyond_thinking(self, query: str, scope: Dict, user_context: Dict) -> Dict[str, Any]:
        """Handle queries that go beyond the application scope"""
        
        # Enhanced prompt for beyond-thinking
        beyond_prompt = self._build_beyond_thinking_prompt(query, scope)
        
        # Use AI engine with expanded context
        conversation_history = []
        ai_response = self.ai_engine.generate_chat_response(
            beyond_prompt, 
            conversation_history,
            style='creative'
        )
        
        # Get expanded suggestions
        expanded_suggestions = self._get_expanded_suggestions(scope)
        
        return {
            'success': True,
            'response': ai_response,
            'related_domains': scope['beyond_domains'],
            'suggested_questions': expanded_suggestions,
            'type': 'beyond_thinking',
            'thinking_scope': scope,
            'timestamp': self._get_timestamp(),
            'is_beyond_application': True
        }

    def _handle_standard_query(self, query: str, user_context: Dict) -> Dict[str, Any]:
        """Handle standard application-specific queries"""
        dashboard_context = self.dashboard_analyzer.identify_dashboard(query)
        enhanced_query = self._enhance_query_with_context(query, dashboard_context, user_context)
        
        conversation_history = []
        ai_response = self.ai_engine.generate_chat_response(
            enhanced_query, 
            conversation_history,
            style='analytical'
        )
        
        dashboard_ids = [dash['id'] for dash in dashboard_context]
        suggested_questions = self.dashboard_analyzer.get_dashboard_suggestions(dashboard_ids)
        
        return {
            'success': True,
            'response': ai_response,
            'related_dashboards': dashboard_context,
            'suggested_questions': suggested_questions,
            'type': 'insight',
            'timestamp': self._get_timestamp(),
            'is_beyond_application': False
        }

    def _build_beyond_thinking_prompt(self, query: str, scope: Dict) -> str:
        """Build enhanced prompt for beyond-thinking queries"""
        
        base_context = """
        You are an advanced AI assistant with expertise in MULTIPLE domains. 
        While you specialize in Steam Analytics, you can think creatively and expansively beyond the application.
        
        YOUR EXPANDED CAPABILITIES:
        1. Creative problem-solving beyond immediate context
        2. Cross-domain knowledge integration
        3. Future trend analysis and predictions
        4. Strategic business thinking
        5. Technical innovation insights
        6. User experience and psychology
        7. Industry analysis and competitive intelligence
        8. Philosophical and conceptual discussions
        
        Always connect insights back to potential value for the Steam Analytics platform when relevant, but don't limit yourself to just that context.
        """
        
        domain_specific_guidance = ""
        if scope['beyond_domains']:
            domains = ", ".join(scope['beyond_domains'])
            domain_specific_guidance = f"\nThis query touches on: {domains}. Provide comprehensive insights across these domains."
        
        prompt = f"""
        {base_context}
        {domain_specific_guidance}
        
        USER QUERY: {query}
        
        THINKING GUIDELINES:
        - Analyze the query from multiple perspectives
        - Connect dots across different domains when relevant
        - Provide innovative ideas and insights
        - Consider both immediate and long-term implications
        - Don't limit yourself to just the Steam Analytics platform
        - Be creative, visionary, and strategically insightful
        
        Provide a response that demonstrates expansive thinking and valuable insights.
        """
        
        return prompt

    def _get_expanded_suggestions(self, scope: Dict) -> List[str]:
        """Get suggestions that encourage beyond-thinking"""
        
        base_suggestions = [
            "How can we apply this to improve our platform?",
            "What are the industry implications?",
            "Any innovative ideas from this insight?",
            "How might this affect future trends?"
        ]
        
        domain_suggestions = {
            'industry_analysis': [
                "Analyze competitor strategies in this area",
                "What market opportunities does this reveal?",
                "How is the gaming industry evolving?"
            ],
            'technical_innovation': [
                "What emerging technologies could enhance this?",
                "How could AI transform this domain?",
                "Technical architecture improvements?"
            ],
            'user_experience': [
                "How would this affect user psychology?",
                "UX design implications?",
                "Accessibility considerations?"
            ],
            'future_trends': [
                "Where is this trend heading in 5 years?",
                "Disruptive possibilities?",
                "Future innovation opportunities?"
            ]
        }
        
        suggestions = base_suggestions.copy()
        for domain in scope['beyond_domains']:
            if domain in domain_suggestions:
                suggestions.extend(domain_suggestions[domain])
        
        return list(dict.fromkeys(suggestions))[:6]

    def _assess_complexity(self, query: str) -> str:
        """Assess query complexity level"""
        word_count = len(query.split())
        
        complex_indicators = [
            'how to', 'why does', 'what if', 'compare', 'analyze', 
            'strategize', 'innovate', 'future of', 'predict'
        ]
        
        if any(indicator in query.lower() for indicator in complex_indicators) or word_count > 15:
            return 'high'
        elif word_count > 8:
            return 'medium'
        else:
            return 'low'

    def _enhance_query_with_context(self, query: str, dashboards: List[Dict], user_context: Dict) -> str:
        """Enhanced context with beyond-thinking awareness"""
        context_parts = []
        
        if dashboards:
            dashboard_names = [f"{dash.get('icon', '📊')} {dash.get('name', 'Dashboard')}" for dash in dashboards]
            context_parts.append(f"Relevant dashboards: {', '.join(dashboard_names)}")
        
        # Always include beyond-thinking capability note
        context_parts.append("You can think beyond immediate Steam Analytics context when beneficial.")
        
        if context_parts:
            enhanced_context = "Context: " + ". ".join(context_parts) + "."
            return f"{enhanced_context}\n\nUser Question: {query}"
        
        return query

    def _create_error_response(self) -> Dict[str, Any]:
        """Create error response with recovery suggestions"""
        return {
            'success': False,
            'response': "I apologize, but I encountered a technical issue. This doesn't limit my thinking capabilities though! What would you like to explore? I can discuss Steam analytics, gaming industry trends, technical innovations, or even broader topics.",
            'suggested_questions': [
                "Let's try a different question",
                "Tell me about gaming industry trends",
                "What technical innovations excite you?",
                "How can we improve user experience?"
            ],
            'type': 'error',
            'timestamp': self._get_timestamp(),
            'is_beyond_application': True
        }

    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        return datetime.now().isoformat()

    def get_welcome_message(self) -> Dict[str, Any]:
        """Get expanded welcome message showcasing beyond-thinking capability"""
        return {
            'success': True,
            'response': """🎮 **Hello! I'm your Unlimited Steam Analytics AI Assistant!**

I specialize in Steam analytics but my thinking isn't limited to just that. I can help you with:

**🎯 Steam Analytics Expertise:**
• Sales trends & revenue analysis
• User behavior & engagement patterns  
• Game performance & genre analytics
• Platform insights & Power BI dashboards

**🚀 Beyond-Thinking Capabilities:**
• Gaming industry trends & competitive analysis
• Technical innovations & AI applications
• User experience design & psychology
• Business strategy & growth opportunities
• Future predictions & emerging technologies
• Creative problem-solving & conceptual discussions

I connect insights across domains to provide truly innovative perspectives. What would you like to explore today?""",
            'suggested_questions': [
                "Show me current Steam sales trends",
                "What's happening in the gaming industry?",
                "How can AI transform game analytics?",
                "Future trends in user engagement",
                "Innovative features for our platform",
                "Let's discuss something creative!"
            ],
            'type': 'expanded_welcome',
            'timestamp': self._get_timestamp(),
            'is_beyond_application': True
        }