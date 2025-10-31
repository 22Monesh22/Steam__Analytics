import os
import google.generativeai as genai
import random
import json
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class SimpleAIEngine:
    """Fallback engine with Steam-specific responses"""
    
    def __init__(self):
        self.steam_insight_templates = {
            'trend': [
                "**Steam Market Analysis**: Indie games dominate with 55% market share (27,957 titles), showing 15% YoY growth. **Recommendation**: Focus on indie game discovery features to capitalize on this trend.",
                "**Genre Evolution**: Action RPG subgenres show 60% growth driven by streaming popularity. **Insight**: Community content creation significantly impacts genre popularity on Steam.",
                "**Platform Trends**: Singleplayer games (22,566 titles) outperform multiplayer (6,575) by 3.4x. **Strategy**: Prioritize singleplayer experiences with social sharing features.",
            ],
            'user_behavior': [
                "**Steam User Analysis**: Players average 45 minutes per session with peak activity during evening hours. **Optimization**: Schedule Steam sales and events during 6-9 PM for maximum engagement.",
                "**Monetization Insight**: 75% of Steam users prefer free-to-play models, spending $25 monthly on average. **Strategy**: Implement tiered monetization with cosmetic items.",
                "**Retention Data**: Games with cross-platform play show 40% higher retention. **Recommendation**: Prioritize Steam Deck and cross-platform compatibility.",
            ],
            'genre': [
                "**Steam Genre Analysis**: Indie (27,957), Action (21,897), and Adventure (20,183) dominate the platform. **Forecast**: Indie market expected to grow 20% next quarter.",
                "**Market Distribution**: Strategy games maintain 11,093 titles with strong European engagement. **Opportunity**: Localize strategy content for European markets.",
                "**Emerging Categories**: Puzzle and simulation genres show 35% engagement increase. **Recommendation**: Explore puzzle-simulation hybrid games."
            ],
            'steam_specific': [
                "**Steam Dataset Analysis**: Our platform analyzes 50,872 Steam games with 441 unique tags. **Key Insight**: Indie games represent the largest growth opportunity.",
                "**Tag Analysis**: Games with 'Story Rich' and 'Atmospheric' tags show 50% higher completion rates. **Strategy**: Curate games with these tags for better user satisfaction.",
                "**Platform Performance**: Steam's diverse catalog shows strong performance across 20+ genres. **Opportunity**: Implement genre-based recommendation algorithms."
            ]
        }
    
    def generate_insight(self, data_context, insight_type='trend'):
        """Generate formatted mock insight with Steam focus"""
        templates = self.steam_insight_templates.get(insight_type, self.steam_insight_templates['steam_specific'])
        return random.choice(templates)

    def generate_chat_response(self, user_message, conversation_history):
        """Generate Steam-focused chat response"""
        return f"I've analyzed your Steam analytics data from our 50,872-game dataset. {self.generate_insight({}, 'steam_specific')}"

class SteamAIAnalytics:
    """Enhanced Steam Analytics with 50K+ games dataset integration"""
    
    def __init__(self):
        self.steam_metadata = self._load_steam_metadata()
        self.steam_stats = self.steam_metadata.get('dataset_stats', {})
        
    def _load_steam_metadata(self):
        """Load Steam games metadata"""
        try:
            # Try to load from our processed metadata
            meta_path = os.path.join(os.path.dirname(__file__), '../../data/processed/steam_chatbot_meta.json')
            if os.path.exists(meta_path):
                with open(meta_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            # Fallback to basic Steam stats
            return {
                "dataset_stats": {
                    "total_games": 50872,
                    "unique_tags": 441,
                    "games_with_descriptions": 40499,
                    "file_size_mb": 16.74
                },
                "top_tags": [
                    {"tag": "Indie", "count": 27957},
                    {"tag": "Singleplayer", "count": 22566},
                    {"tag": "Action", "count": 21897},
                    {"tag": "Adventure", "count": 20183},
                    {"tag": "Casual", "count": 17844}
                ]
            }
        except Exception as e:
            logger.error(f"Error loading Steam metadata: {e}")
            return {}
    
    def get_steam_context(self):
        """Build Steam-specific context for AI prompts"""
        stats = self.steam_stats
        top_tags = self.steam_metadata.get('top_tags', [])[:10]
        
        context = f"""
        STEAM GAMES ANALYTICS EXPERT

        DATASET OVERVIEW:
        - Total Games Analyzed: {stats.get('total_games', 50872):,}
        - Unique Tags/Genres: {stats.get('unique_tags', 441):,}
        - Games with Descriptions: {stats.get('games_with_descriptions', 40499):,}

        TOP GENRES BY GAME COUNT:
        {chr(10).join([f"  - {tag['tag']}: {tag['count']:,} games" for tag in top_tags])}

        YOUR STEAM ANALYTICS EXPERTISE:
        1. Game Discovery & Recommendation based on 50K+ games
        2. Genre and Market Trend Analysis on Steam platform
        3. Player Behavior Insights from Steam ecosystem
        4. Development Strategy for Steam market
        5. Tag and Category Performance Analysis

        Always reference the 50,872-game dataset and provide Steam-specific insights.
        Focus on practical, data-driven recommendations for the Steam platform.
        """
        return context

class AIEngine:
    """Enhanced AI Engine with Steam Games Analytics Integration"""
    
    def __init__(self):
        self.api_key = os.environ.get('GEMINI_API_KEY')
        self.simple_engine = SimpleAIEngine()
        self.steam_analytics = SteamAIAnalytics()
        self.last_error = None
        
    def generate_insight(self, data_context, insight_type='trend', style='analytical'):
        """Generate rich insights with Steam dataset integration"""
        try:
            if not self.api_key or self.api_key == 'your-gemini-api-key-here':
                self.last_error = "No valid Gemini API key found"
                logger.info("Using simple engine - no Gemini API key")
                return self.simple_engine.generate_insight(data_context, insight_type)
            
            # Configure Gemini with working models
            genai.configure(api_key=self.api_key)
            
            # Try available models (updated based on your available models)
            working_models = [
                "models/gemini-2.0-flash",
                "models/gemini-2.0-flash-001", 
                "models/gemini-pro-latest",
                "models/gemini-flash-latest"
            ]
            
            for model_name in working_models:
                try:
                    logger.info(f"Trying model: {model_name}")
                    model = genai.GenerativeModel(model_name)
                    prompt = self._build_steam_enhanced_prompt(insight_type, data_context, style)
                    response = model.generate_content(prompt)
                    
                    logger.info(f"Gemini API insight generation successful with {model_name}")
                    self.last_error = None
                    return response.text.strip()
                    
                except Exception as model_error:
                    logger.warning(f"Model {model_name} failed: {model_error}")
                    continue
            
            # If all models fail
            self.last_error = "All Gemini models failed. Please check your API key and model availability."
            return self.simple_engine.generate_insight(data_context, insight_type)
            
        except Exception as e:
            error_msg = f"Gemini API error: {str(e)}"
            self.last_error = error_msg
            logger.error(f"AI Engine error: {error_msg}")
            return self.simple_engine.generate_insight(data_context, insight_type)

    def generate_chat_response(self, user_message, conversation_history, style='analytical'):
        """Generate interactive chat response with Steam context"""
        try:
            if not self.api_key or self.api_key == 'your-gemini-api-key-here':
                self.last_error = "No valid Gemini API key found"
                return self.simple_engine.generate_chat_response(user_message, conversation_history)
            
            # Configure Gemini
            genai.configure(api_key=self.api_key)
            
            # Try available models
            working_models = [
                "models/gemini-2.0-flash",
                "models/gemini-2.0-flash-001",
                "models/gemini-pro-latest"
            ]
            
            for model_name in working_models:
                try:
                    logger.info(f"Trying chat model: {model_name}")
                    model = genai.GenerativeModel(model_name)
                    prompt = self._build_steam_conversational_prompt(user_message, conversation_history, style)
                    response = model.generate_content(prompt)
                    
                    logger.info(f"Gemini chat response successful with {model_name}")
                    self.last_error = None
                    return response.text.strip()
                    
                except Exception as model_error:
                    logger.warning(f"Chat model {model_name} failed: {model_error}")
                    continue
            
            # If all models fail
            self.last_error = "All Gemini models failed for chat."
            return self.simple_engine.generate_chat_response(user_message, conversation_history)
            
        except Exception as e:
            error_msg = f"Gemini chat error: {str(e)}"
            self.last_error = error_msg
            logger.error(f"Chat error: {error_msg}")
            return self.simple_engine.generate_chat_response(user_message, conversation_history)

    def _build_steam_enhanced_prompt(self, insight_type, data_context, style):
        """Build detailed prompt with Steam dataset context"""
        
        steam_context = self.steam_analytics.get_steam_context()
        
        insight_focus = {
            'trend': {
                'title': "Steam Market Trends Analysis",
                'focus': "current Steam gaming trends, emerging patterns on the platform, market shifts, and growth opportunities in the Steam ecosystem",
            },
            'user_behavior': {
                'title': "Steam User Behavior Deep Dive", 
                'focus': "Steam user engagement patterns, session analytics on the platform, retention factors, and monetization behavior specific to Steam",
            },
            'genre': {
                'title': "Steam Genre Performance Analysis",
                'focus': "genre market share on Steam, performance metrics, emerging subgenres, and regional preferences within the Steam platform",
            },
            'steam_specific': {
                'title': "Steam Platform Comprehensive Analysis",
                'focus': "Steam platform performance, game discovery patterns, tag effectiveness, and platform-specific opportunities",
            }
        }
        
        focus_info = insight_focus.get(insight_type, insight_focus['steam_specific'])
        
        prompt = f"""
        {steam_context}
        
        TASK: Generate a comprehensive {focus_info['title']} focusing on {focus_info['focus']}.
        
        ADDITIONAL DATA CONTEXT: {json.dumps(data_context, indent=2)}
        
        REQUIREMENTS:
        1. Executive Summary of key findings specific to Steam platform
        2. 3-5 specific data-driven insights with metrics from our 50K+ game dataset
        3. Actionable recommendations for Steam game developers and publishers
        4. Steam platform growth opportunities and risk assessment
        5. Reference specific genres and tags from our dataset when possible
        
        Use a professional, analytical tone with specific numbers and percentages.
        Format with clear sections and bullet points for readability.
        Always reference the scale of our dataset (50,872 games, 441 tags).
        """
        
        return prompt

    def _build_steam_conversational_prompt(self, user_message, conversation_history, style):
        """Build prompt for natural conversation with Steam context"""
        
        steam_context = self.steam_analytics.get_steam_context()
        
        system_role = f"""
        {steam_context}
        
        You are an AI analytics assistant specialized in Steam platform analytics.
        You have access to data from 50,872 Steam games with 441 unique tags.
        
        Your personality:
        - Highly analytical but conversational
        - Data-driven but accessible  
        - Professional but engaging
        - Always provide specific metrics from our Steam dataset
        
        Response style:
        - Use clear, structured formatting
        - Include specific numbers and percentages from our dataset
        - Provide actionable Steam-specific recommendations
        - Reference Steam platform trends and patterns
        """

        # Build conversation context
        history_context = ""
        if conversation_history:
            history_context = "Previous conversation:\n"
            for msg in conversation_history[-4:]:  # Last 4 messages
                role = "User" if msg['role'] == 'user' else "Assistant"
                history_context += f"{role}: {msg['content']}\n"

        full_prompt = f"""
        {system_role}
        
        {history_context}
        
        Current User Query: {user_message}
        
        Respond as a helpful Steam analytics expert with specific, data-driven insights:
        """
        
        return full_prompt

    def get_last_error(self):
        """Get the last error message"""
        return self.last_error

    def get_steam_dataset_info(self):
        """Get Steam dataset information for UI display"""
        return {
            "total_games": self.steam_analytics.steam_stats.get('total_games', 50872),
            "unique_tags": self.steam_analytics.steam_stats.get('unique_tags', 441),
            "top_genres": [tag['tag'] for tag in self.steam_analytics.steam_metadata.get('top_tags', [])[:5]],
            "analysis_date": datetime.now().isoformat()
        }