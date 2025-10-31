import os
import google.generativeai as genai
import json
from config import Config

class AIInsights:
    def __init__(self):
        self.api_key = os.environ.get('GEMINI_API_KEY') or Config.GEMINI_API_KEY
        print(f"✅ AI Insights initialized. API Key: {'Configured' if self.api_key and self.api_key != 'your-gemini-api-key-here' else 'Not configured'}")
        
    def generate_insights(self, data_type, data):
        """Generate real AI insights using Gemini API"""
        try:
            if not self.api_key or self.api_key == 'your-gemini-api-key-here':
                print("❌ No valid Gemini API key found")
                return self._get_error_response("Please configure your Gemini API key in the .env file")
            
            # Configure Gemini
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel('gemini-pro')
            
            # Build prompt with actual data
            prompt = self._build_prompt(data_type, data)
            
            # Generate response
            response = model.generate_content(prompt)
            
            print("✅ Gemini API call successful")
            return self._parse_response(response.text, data_type)
            
        except Exception as e:
            print(f"❌ Gemini API error: {e}")
            return self._get_error_response(f"API Error: {str(e)}")

    def _build_prompt(self, data_type, data):
        """Build detailed prompt for Gemini API"""
        
        prompt_templates = {
            'user_clusters': """
            Analyze this user clustering data from a gaming platform and provide comprehensive insights:
            
            DATA: {data}
            
            Please provide:
            1. **Executive Summary** - Main patterns in user segmentation
            2. **Key Findings** - 3-5 specific insights about user behavior
            3. **Opportunities** - Potential areas for growth and engagement
            4. **Recommendations** - Actionable strategies for each user segment
            
            Focus on data-driven insights and practical recommendations.
            """,
            
            'game_popularity': """
            Analyze this game popularity data and provide strategic insights:
            
            DATA: {data}
            
            Please provide:
            1. **Market Overview** - Current trends in game popularity
            2. **Key Patterns** - What makes games successful
            3. **Emerging Opportunities** - Untapped genres or features
            4. **Strategic Recommendations** - How to leverage popularity data
            
            Include specific metrics and growth predictions.
            """,
            
            'trends': """
            Analyze these gaming platform trends and provide forward-looking insights:
            
            DATA: {data}
            
            Please provide:
            1. **Trend Analysis** - Current market movements
            2. **Growth Indicators** - Key metrics showing platform health
            3. **Predictions** - Where the market is heading
            4. **Strategic Actions** - Recommendations for capitalizing on trends
            
            Be specific and data-focused.
            """
        }
        
        template = prompt_templates.get(data_type, """
        Analyze this gaming data and provide comprehensive insights:
        
        DATA: {data}
        
        Provide a structured analysis with key findings and recommendations.
        """)
        
        # Format data for the prompt
        formatted_data = json.dumps(data, indent=2) if data else "No data provided"
        
        return template.format(data=formatted_data)

    def _parse_response(self, text, data_type):
        """Parse Gemini response into structured format"""
        try:
            # For now, return the raw text with some structure
            # You can enhance this parsing based on your needs
            return {
                "summary": text,
                "key_findings": self._extract_key_points(text),
                "predictions": self._extract_predictions(text),
                "recommendations": self._extract_recommendations(text),
                "raw_response": text,
                "data_type": data_type,
                "source": "Gemini AI"
            }
        except Exception as e:
            return self._get_error_response(f"Response parsing error: {str(e)}")

    def _extract_key_points(self, text):
        """Extract key points from response (basic implementation)"""
        # This is a simple extraction - you can make it more sophisticated
        lines = text.split('\n')
        key_points = []
        for line in lines:
            if any(keyword in line.lower() for keyword in ['key', 'finding', 'insight', 'important', 'notable']):
                if len(line.strip()) > 20:  # Avoid very short lines
                    key_points.append(line.strip())
        
        return key_points[:5] if key_points else ["Analysis completed successfully"]

    def _extract_predictions(self, text):
        """Extract predictions from response"""
        lines = text.split('\n')
        predictions = []
        for line in lines:
            if any(keyword in line.lower() for keyword in ['predict', 'forecast', 'expect', 'will grow', 'trending']):
                if len(line.strip()) > 20:
                    predictions.append(line.strip())
        
        return predictions[:3] if predictions else ["Continued growth expected"]

    def _extract_recommendations(self, text):
        """Extract recommendations from response"""
        lines = text.split('\n')
        recommendations = []
        for line in lines:
            if any(keyword in line.lower() for keyword in ['recommend', 'suggest', 'should', 'advise', 'consider']):
                if len(line.strip()) > 20:
                    recommendations.append(line.strip())
        
        return recommendations[:4] if recommendations else ["Monitor performance and adjust strategy"]

    def _get_error_response(self, error_message):
        """Return error response structure"""
        return {
            "summary": f"Unable to generate insights: {error_message}",
            "key_findings": ["Analysis failed due to API issue"],
            "predictions": ["Please check API configuration"],
            "recommendations": ["Verify your Gemini API key and try again"],
            "error": error_message,
            "source": "Error"
        }

# Example usage
if __name__ == "__main__":
    # Test the AI insights
    ai = AIInsights()
    
    test_data = {
        "total_users": 10000,
        "active_users": 6500,
        "new_signups": 500,
        "popular_genres": ["RPG", "Strategy", "Action"]
    }
    
    result = ai.generate_insights('trends', test_data)
    print("Generated Insights:")
    print(json.dumps(result, indent=2))