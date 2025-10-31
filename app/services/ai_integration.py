# app/services/ai_integration.py
import logging
import google.generativeai as genai
from flask import current_app
import os

logger = logging.getLogger(__name__)

class GeminiService:
    """Enhanced Gemini AI service for dashboard analysis"""
    
    def __init__(self):
        self.api_key = current_app.config.get('GEMINI_API_KEY') or os.getenv('GEMINI_API_KEY')
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        else:
            logger.warning("GEMINI_API_KEY not configured")
            self.model = None
    
    def generate_response(self, prompt: str, max_tokens: int = 1000) -> str:
        """Generate AI response with error handling"""
        try:
            if not self.model:
                return self._get_fallback_response()
            
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=max_tokens,
                    temperature=0.3
                )
            )
            
            return response.text if response else self._get_fallback_response()
            
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            return self._get_fallback_response()
    
    def _get_fallback_response(self) -> str:
        """Fallback response when AI is unavailable"""
        return "I specialize in Power BI dashboard analysis. Based on typical gaming analytics dashboards, I can help you interpret metrics like user engagement, revenue trends, and player behavior. What specific aspect of your dashboard would you like to explore?"