import google.generativeai as genai
import os
from typing import Dict, List, Tuple
import re
from datetime import datetime

class PowerBILlmAgent:
    def __init__(self):
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        self.conversation_history = {}
        
        if self.gemini_api_key:
            try:
                genai.configure(api_key=self.gemini_api_key)
                self.model = genai.GenerativeModel('models/gemini-2.0-flash')
                self.use_real_llm = True
                print("✅ Interactive LLM Agent Initialized")
            except Exception as e:
                print(f"⚠️ LLM init failed: {e}")
                self.use_real_llm = False
        else:
            self.use_real_llm = False
        
        # Enhanced dashboard configurations with REAL insights
        self.dashboards = {
            'game-analytics': {
                'name': 'The Popularity Playbook',
                'data_context': """
                POWER BI DASHBOARD INSIGHTS:
                
                📊 CHARTS & METRICS:
                • Rating Landscape of Games (Bar Chart) - Shows game count by rating buckets
                • Distribution of Game Ratings (Donut Chart) - Rating distribution percentages
                • Typical Game Cost: Average pricing analysis
                • Player Approval Score: User satisfaction metrics
                • Market Trust Factor: Market confidence indicators
                
                🎯 HOW TO USE THIS DASHBOARD:
                • Use filters to analyze specific game genres or price ranges
                • Click on chart segments to drill down into details
                • Hover over bars to see exact counts and percentages
                • Compare rating distributions across different game categories
                """
            },
            'user-analytics': {
                'name': 'Dynamics of User Contribution',
                'data_context': """
                POWER BI DASHBOARD INSIGHTS:
                
                📊 CHARTS & METRICS:
                • Engagement by User Segment (Clustered Column Chart) - User activity comparison
                • User Segments: Different user categories and their engagement levels
                • Total Active Users: Overall user base metrics
                • Review counts by segment: User contribution analysis
                
                🎯 HOW TO USE THIS DASHBOARD:
                • Filter by user segment to focus on specific groups
                • Use date filters to analyze trends over time
                • Compare product ownership vs engagement hours
                • Identify which segments contribute most reviews and activity
                """
            },
            'recommendation-engine': {
                'name': 'Trend Analysis Dashboard', 
                'data_context': """
                POWER BI DASHBOARD INSIGHTS:
                
                📊 CHARTS & METRICS:
                • Monthly User Engagement Trend (Bar Chart) - Temporal activity patterns
                • User Activity by Day of Week (Column Chart) - Weekly engagement cycles
                • Average Playtime: User engagement duration metrics
                • Market Trust Factor: Platform confidence indicators
                
                🎯 HOW TO USE THIS DASHBOARD:
                • Analyze seasonal patterns in user engagement
                • Plan resources based on weekly activity patterns
                • Track playtime trends to measure engagement quality
                • Use time filters to compare different periods
                """
            }
        }

    def _create_interactive_prompt(self, user_question: str, dashboard_name: str, data_context: str, conversation_context: Dict) -> str:
        """Create enhanced prompt with Power BI guidance"""
        
        context_summary = ""
        if conversation_context.get('last_topic'):
            context_summary = f"\nPrevious discussion: {conversation_context['last_topic']}"
        
        return f"""
        You are a Power BI dashboard expert and data analyst. Your role is to help users understand and navigate Power BI dashboards while providing data insights.

        📊 CURRENT DASHBOARD: {dashboard_name}
        {data_context}
        {context_summary}

        ❓ USER QUESTION: {user_question}

        🎯 RESPONSE GUIDELINES:

        1. **POWER BI GUIDANCE** (if user asks about using the dashboard):
           - Explain how to interact with specific charts
           - Describe filter and navigation options
           - Provide step-by-step instructions for common tasks
           - Explain what each chart/metric represents

        2. **DATA INSIGHTS** (if user asks about the data):
           - Provide insights based on the dashboard metrics
           - Explain trends and patterns visible in the charts
           - Offer business implications of the findings
           - Suggest related analyses

        3. **BE INTERACTIVE & HELPFUL**:
           - Use natural, engaging language
           - Ask follow-up questions to explore further
           - Use emojis tastefully to enhance engagement
           - Structure responses for easy reading

        Now provide a helpful, engaging response:
        """

    def _update_conversation_context(self, user_id: str, user_question: str, response: str) -> Dict:
        """Update conversation context"""
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = {
                'last_topic': '',
                'topics_discussed': [],
                'last_interaction': datetime.now()
            }
        
        main_topic = self._extract_topic(user_question)
        
        self.conversation_history[user_id].update({
            'last_topic': main_topic,
            'last_interaction': datetime.now(),
            'topics_discussed': list(set(self.conversation_history[user_id]['topics_discussed'] + [main_topic]))
        })
        
        return self.conversation_history[user_id]

    def _extract_topic(self, question: str) -> str:
        """Extract main topic from user question"""
        question_lower = question.lower()
        
        # Power BI usage topics
        if any(word in question_lower for word in ['how to', 'use', 'navigate', 'filter', 'chart', 'graph', 'dashboard']):
            return 'powerbi_guidance'
        elif any(word in question_lower for word in ['genre', 'category', 'type']):
            return 'game_genres'
        elif any(word in question_lower for word in ['player', 'user', 'retention', 'engagement']):
            return 'player_analytics'
        elif any(word in question_lower for word in ['revenue', 'sales', 'money', 'profit', 'price']):
            return 'revenue_analysis'
        elif any(word in question_lower for word in ['trend', 'growth', 'performance', 'time']):
            return 'performance_trends'
        elif any(word in question_lower for word in ['popular', 'top', 'best', 'trending', 'rating']):
            return 'popular_content'
        else:
            return 'general_analysis'

    def analyze_with_llm(self, user_question: str, dashboard_name: str, data_context: str, conversation_context: Dict) -> str:
        """Use LLM for Power BI guidance and insights"""
        if self.use_real_llm and self.model:
            try:
                prompt = self._create_interactive_prompt(user_question, dashboard_name, data_context, conversation_context)
                response = self.model.generate_content(prompt)
                return response.text
            except Exception as e:
                print(f"LLM failed: {e}")
                return self._get_enhanced_fallback(user_question, dashboard_name)
        else:
            return self._get_enhanced_fallback(user_question, dashboard_name)

    def _get_enhanced_fallback(self, user_question: str, dashboard_name: str) -> str:
        """Enhanced fallback with Power BI guidance"""
        question_lower = user_question.lower()
        
        # Power BI Guidance Questions
        if any(word in question_lower for word in ['how to', 'use', 'navigate']):
            return f"""🛠️ **Power BI Dashboard Guidance - {dashboard_name}**

**Getting Started:**
• Click on any chart to see detailed tooltips
• Use the filter pane to focus on specific data
• Hover over chart elements for exact values
• Use the drill-down feature by clicking on chart segments

**Specific Features:**
• **Filtering**: Use filters to select specific time periods, genres, or user segments
• **Zoom**: Click and drag on charts to zoom into specific areas  
• **Export**: Use the export button to save reports
• **Bookmarks**: Save your current view for quick access

**Need help with a specific chart?** Ask me about any particular visualization!"""

        elif 'filter' in question_lower:
            return f"""🔍 **Filtering Guide - {dashboard_name}**

**How to Filter Data:**

1. **Find the Filter Pane**: Look for the filter panel on the dashboard
2. **Select Filters**: Choose from available options like:
   - Time periods (months, years)
   - Game genres or categories  
   - User segments or regions
   - Rating ranges or price brackets

3. **Apply Multiple Filters**: Combine filters for precise analysis
4. **Clear Filters**: Use the "Clear all" button to reset

**Pro Tip**: Filters affect all charts simultaneously, letting you see how different segments perform across all metrics!"""

        elif any(word in question_lower for word in ['chart', 'graph', 'visualization']):
            return f"""📈 **Chart Interpretation - {dashboard_name}**

**Understanding the Visualizations:**

• **Bar Charts**: Compare quantities across categories (longer bars = larger values)
• **Donut/Pie Charts**: Show percentage distributions of whole
• **Column Charts**: Similar to bar charts but vertical orientation
• **Trend Lines**: Show patterns over time (upward = growth)

**How to Read Charts:**
- Hover over any element to see exact numbers
- Colors typically represent different categories
- Axis labels show what's being measured
- Legends explain what each color represents

**Want me to explain a specific chart?** Tell me which one!"""

        elif 'what does this dashboard' in question_lower:
            return f"""🎯 **{dashboard_name} - Overview**

This dashboard helps you analyze:

**📊 Key Focus Areas:**
- Game popularity and market reception
- User engagement patterns and segments  
- Temporal trends and seasonal patterns
- Rating distributions and player satisfaction

**💡 Business Applications:**
- Identify successful game characteristics
- Understand user behavior and preferences
- Optimize pricing and marketing strategies
- Plan resource allocation based on trends

**Ask me about specific metrics or how to find particular insights!**"""

        else:
            return f"""🤔 **Let's Explore Your Power BI Dashboard!**

I can help you with:

**🛠️ Power BI Usage:**
- How to filter and navigate the dashboard
- Understanding charts and visualizations  
- Exporting data and reports
- Advanced features and tips

**📈 Data Insights:**
- Interpreting the metrics and KPIs
- Identifying trends and patterns
- Business implications of the data
- Comparative analysis

**💡 Try asking:**
- "How do I filter to see specific data?"
- "What does this chart show?"
- "How to compare different segments?"
- "What are the key trends in this data?"

What would you like to explore?"""

    def process_query(self, user_question: str, dashboard_type: str, user_id: str = "default") -> Dict:
        """Process user query with Power BI context"""
        dashboard_info = self.dashboards.get(dashboard_type, self.dashboards['game-analytics'])
        data_context = dashboard_info.get('data_context', '')
        
        # Get conversation context
        conversation_context = self.conversation_history.get(user_id, {})
        
        # Generate response
        response = self.analyze_with_llm(user_question, dashboard_info['name'], data_context, conversation_context)
        
        # Update conversation context
        updated_context = self._update_conversation_context(user_id, user_question, response)
        
        return {
            'success': True,
            'response': response,
            'dashboard_used': dashboard_info['name'],
            'suggestions': self._get_interactive_suggestions(user_question, updated_context, dashboard_type),
            'conversation_context': {
                'last_topic': updated_context.get('last_topic', ''),
                'topics_discussed': updated_context.get('topics_discussed', [])
            }
        }

    def _get_interactive_suggestions(self, question: str, conversation_context: Dict, dashboard_type: str) -> List[str]:
        """Get context-aware interactive suggestions"""
        question_lower = question.lower()
        last_topic = conversation_context.get('last_topic', '')
        
        # Power BI guidance suggestions
        if any(word in question_lower for word in ['how to', 'use', 'navigate']) or last_topic == 'powerbi_guidance':
            return [
                "How to filter data", 
                "Explain chart types",
                "Export reports guide",
                "Dashboard navigation tips"
            ]
        
        # Data analysis suggestions based on dashboard type
        if dashboard_type == 'game-analytics':
            return [
                "Analyze rating distribution",
                "Compare game prices", 
                "Market trust factors",
                "Popularity trends"
            ]
        elif dashboard_type == 'user-analytics':
            return [
                "User segment analysis",
                "Engagement patterns", 
                "Review contribution",
                "Segment comparisons"
            ]
        elif dashboard_type == 'recommendation-engine':
            return [
                "Monthly engagement trends",
                "Weekly activity patterns", 
                "Playtime analysis",
                "Seasonal trends"
            ]
        else:
            return [
                "Dashboard overview",
                "Key metrics explanation", 
                "Data navigation",
                "Business insights"
            ]