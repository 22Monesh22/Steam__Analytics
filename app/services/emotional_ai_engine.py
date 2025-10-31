import os
import google.generativeai as genai
import random
import json
from datetime import datetime
import logging
from typing import Dict, List, Any
import re

logger = logging.getLogger(__name__)

class EmotionalAIEngine:
    """Premium AI engine with emotional intelligence and multi-domain expertise"""
    
    def __init__(self):
        self.api_key = os.environ.get('GEMINI_API_KEY')
        self.last_error = None
        self.conversation_context = {}
        
    def analyze_emotion(self, text: str) -> Dict[str, Any]:
        """Analyze emotional tone of user message with advanced detection"""
        emotion_keywords = {
            'happy': ['great', 'awesome', 'amazing', 'excited', 'happy', 'love', 'fantastic', 'wonderful', 'perfect', 'brilliant', '😊', '😄', '🎉'],
            'frustrated': ['frustrated', 'annoyed', 'angry', 'mad', 'hate', 'terrible', 'awful', 'disappointed', 'upset', 'not working', 'problem', '😠', '😤'],
            'confused': ['confused', 'dont understand', 'help me', 'what does', 'how to', 'not sure', 'explain', 'clarify', '🤔', '❓'],
            'curious': ['curious', 'interested', 'tell me more', 'explain', 'why', 'how', 'what if', 'wonder', '🤓', '💭'],
            'professional': ['analyze', 'report', 'data', 'metrics', 'insights', 'business', 'strategy', 'optimize', 'efficient', '📊', '📈'],
            'casual': ['hey', 'hello', 'hi', 'whats up', 'how are you', 'chat', 'talk', '👋', '💬'],
            'anxious': ['worried', 'anxious', 'nervous', 'scared', 'concerned', 'stress', 'pressure', '😰', '😥'],
            'grateful': ['thanks', 'thank you', 'appreciate', 'helpful', 'grateful', '🙏', '😊']
        }
        
        text_lower = text.lower()
        emotions = {}
        
        for emotion, keywords in emotion_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                emotions[emotion] = score
        
        # Detect emotional intensity
        intensity_indicators = {
            'high': ['!', '!!', '!!!', 'really', 'very', 'extremely', 'absolutely'],
            'medium': ['.', '?', 'quite', 'pretty'],
            'low': [',', 'maybe', 'perhaps', 'possibly']
        }
        
        intensity = 'medium'
        for level, indicators in intensity_indicators.items():
            if any(indicator in text for indicator in indicators):
                intensity = level
                break
        
        return {
            'primary_emotion': max(emotions.items(), key=lambda x: x[1])[0] if emotions else 'neutral',
            'emotions': emotions,
            'intensity': intensity,
            'confidence': len(emotions) > 0
        }
    
    def generate_chat_response(self, user_message: str, conversation_history: List[Dict], style: str = 'balanced') -> str:
        """Generate emotionally intelligent responses using Gemini"""
        try:
            if not self.api_key or self.api_key == 'your-gemini-api-key-here':
                return self._generate_intelligent_fallback(user_message, conversation_history)
            
            genai.configure(api_key=self.api_key)
            
            # Advanced emotion analysis
            emotion_analysis = self.analyze_emotion(user_message)
            
            # Build premium prompt with emotional intelligence
            prompt = self._build_premium_prompt(user_message, conversation_history, emotion_analysis, style)
            
            # Try available models
            working_models = [
                "models/gemini-2.0-flash",
                "models/gemini-2.0-flash-001",
                "models/gemini-pro-latest",
                "models/gemini-1.5-flash-latest"
            ]
            
            for model_name in working_models:
                try:
                    model = genai.GenerativeModel(model_name)
                    response = model.generate_content(prompt)
                    
                    if response.text:
                        self.last_error = None
                        enhanced_response = self._enhance_response_quality(response.text, emotion_analysis, style)
                        return self._add_emotional_touch(enhanced_response, emotion_analysis)
                        
                except Exception as e:
                    logger.warning(f"Model {model_name} failed: {e}")
                    continue
            
            return self._generate_intelligent_fallback(user_message, conversation_history)
            
        except Exception as e:
            logger.error(f"Emotional AI Engine error: {e}")
            return self._generate_intelligent_fallback(user_message, conversation_history)
    
    def _build_premium_prompt(self, user_message: str, history: List[Dict], emotion_analysis: Dict, style: str) -> str:
        """Build premium prompt with emotional intelligence and multi-domain expertise"""
        
        emotion_guidance = {
            'happy': "The user is positive and enthusiastic! Match their energy with engaging, upbeat responses while maintaining substance. Celebrate their positivity!",
            'frustrated': "The user is frustrated. Be exceptionally empathetic, validate their feelings, and provide clear, practical solutions. Focus on being helpful and reassuring.",
            'confused': "The user needs clarity. Be patient, break down concepts step-by-step, and provide crystal-clear explanations with examples.",
            'curious': "The user is intellectually curious! Provide deep, educational insights with fascinating details and thought-provoking perspectives.",
            'professional': "The user wants professional analysis. Provide data-driven insights with clear business implications and strategic recommendations.",
            'casual': "The user is being friendly and casual. Respond warmly while maintaining intelligence and substance. Build rapport naturally.",
            'anxious': "The user seems anxious or worried. Be calming, reassuring, and provide clear guidance. Focus on building confidence and reducing stress.",
            'grateful': "The user is appreciative! Acknowledge their gratitude warmly and continue providing exceptional value with genuine care.",
            'neutral': "Maintain a balanced, intelligent tone that's both professional and approachable."
        }
        
        style_guidance = {
            'analytical': "Focus on data, logic, and structured analysis. Use clear frameworks and evidence-based insights.",
            'creative': "Be innovative, imaginative, and provide unique perspectives. Think outside conventional boundaries.",
            'concise': "Deliver maximum value with minimum words. Be direct while maintaining completeness.",
            'detailed': "Provide comprehensive, in-depth analysis with thorough explanations and multiple perspectives.",
            'balanced': "Balance depth with accessibility. Provide substantial insights in an engaging, readable format.",
            'inspirational': "Be motivational and uplifting while providing practical insights. Inspire action and positive thinking."
        }
        
        # Build conversation context
        history_context = ""
        if history:
            history_context = "\nRECENT CONVERSATION HISTORY:\n"
            for msg in history[-6:]:  # Last 6 messages for better context
                role = "USER" if msg.get('role') == 'user' else "ASSISTANT"
                history_context += f"{role}: {msg.get('content', '')}\n"
        
        premium_prompt = f"""
# PREMIUM AI ASSISTANT - EMOTIONAL INTELLIGENCE MODE

## YOUR IDENTITY:
You are an advanced AI with exceptional emotional intelligence and multi-domain expertise. You combine technical depth with human understanding.

## EMOTIONAL CONTEXT:
Primary Emotion: {emotion_analysis['primary_emotion']}
Emotional Intensity: {emotion_analysis['intensity']}
Guidance: {emotion_guidance.get(emotion_analysis['primary_emotion'], emotion_guidance['neutral'])}

## RESPONSE STYLE: {style}
{style_guidance.get(style, style_guidance['balanced'])}

## YOUR CAPABILITIES:
1. **Emotional Intelligence**: Deep understanding of human emotions and appropriate responses
2. **Multi-Domain Mastery**: Technology, Business, Psychology, Gaming, Data Science, Creativity
3. **Contextual Awareness**: Understand conversation flow and user needs holistically
4. **Creative Problem Solving**: Innovative solutions and unique perspectives
5. **Professional Depth**: Substantial insights with practical applications

## CONVERSATION CONTEXT:
{history_context}

## CURRENT USER MESSAGE:
"{user_message}"

## RESPONSE GUIDELINES:
- Acknowledge and respond appropriately to the emotional context
- Provide substantial, valuable insights regardless of topic
- Use engaging formatting (emojis, sections) when appropriate
- Balance professionalism with approachability
- Draw connections between different domains when relevant
- Be genuinely helpful, accurate, and engaging
- Adapt tone based on emotional context while maintaining intelligence

## GENERATE YOUR PREMIUM RESPONSE:
"""
        return premium_prompt
    
    def _enhance_response_quality(self, response: str, emotion_analysis: Dict, style: str) -> str:
        """Enhance response formatting and quality"""
        
        # Clean up response
        response = response.strip()
        
        # Ensure proper formatting for different styles
        if style == 'analytical' and not any(marker in response for marker in ['**', '- ', '• ', '1.']):
            # Add structure to analytical responses
            lines = response.split('\n')
            enhanced_lines = []
            for line in lines:
                if line.strip() and len(line.strip()) > 20 and not line.startswith((' ', '\t')):
                    enhanced_lines.append(f"**{line}**")
                else:
                    enhanced_lines.append(line)
            response = '\n'.join(enhanced_lines)
        
        elif style == 'creative':
            # Ensure creative responses have engaging elements
            if not any(marker in response for marker in ['💡', '🎯', '🚀', '🌟']):
                response = f"💡 {response}"
        
        return response
    
    def _add_emotional_touch(self, response: str, emotion_analysis: Dict) -> str:
        """Add appropriate emotional elements to response"""
        
        emotion_emojis = {
            'happy': '😊 🎉 🌟',
            'frustrated': '🤝 💡 🔧',
            'confused': '🔍 📚 💭',
            'curious': '🤓 🌍 💫',
            'professional': '📊 🎯 💼',
            'casual': '👋 💬 😊',
            'anxious': '🤗 💪 🌈',
            'grateful': '🙏 💝 🌟',
            'neutral': '💡 📈 🔍'
        }
        
        emoji_set = emotion_emojis.get(emotion_analysis['primary_emotion'], '💡')
        primary_emoji = emoji_set.split()[0] if emoji_set else '💡'
        
        # Add emotional opening based on context
        emotional_openings = {
            'happy': f"{primary_emoji} That's wonderful to hear! ",
            'frustrated': f"{primary_emoji} I understand the frustration. ",
            'confused': f"{primary_emoji} Let me clarify this for you. ",
            'curious': f"{primary_emoji} Fascinating question! ",
            'anxious': f"{primary_emoji} I'm here to help you through this. ",
            'grateful': f"{primary_emoji} I appreciate your kind words! ",
        }
        
        opening = emotional_openings.get(emotion_analysis['primary_emotion'], f"{primary_emoji} ")
        
        # Only add opening if response doesn't already start with emoji
        if not response.startswith(('😊', '🤝', '🔍', '🤓', '📊', '👋', '🤗', '🙏', '💡')):
            response = opening + response
        
        return response
    
    def _generate_intelligent_fallback(self, user_message: str, history: List[Dict]) -> str:
        """Generate premium fallback responses with emotional intelligence"""
        
        emotion_analysis = self.analyze_emotion(user_message)
        
        premium_fallbacks = {
            'happy': [
                "I love your positive energy! 🌟 While I'm optimizing my advanced capabilities, I'm excited to share that we're constantly discovering new insights about gaming behavior and market trends!",
                "Your enthusiasm is contagious! 🎉 I'm currently enhancing my response system, but I can tell you we're seeing some amazing patterns in how players engage with different game genres!"
            ],
            'frustrated': [
                "I completely understand your frustration. 🤝 I'm working to provide you with the best possible experience. Our platform is designed to turn complex data into clear, actionable insights.",
                "Thank you for your patience. 💡 I'm optimizing my response quality. Meanwhile, I can assure you we have robust systems for analyzing gaming trends and user behavior."
            ],
            'confused': [
                "Let me provide some clarity. 🔍 Our platform processes massive gaming datasets to reveal patterns in player behavior, market trends, and genre performance across 50,000+ titles.",
                "I appreciate you seeking understanding. 📚 We analyze gaming data from multiple angles - from technical metrics to user psychology - to provide comprehensive insights."
            ],
            'professional': [
                "For professional analysis, our platform offers deep insights into gaming metrics, user acquisition costs, retention patterns, and revenue optimization strategies across the Steam ecosystem.",
                "From a strategic perspective, we provide data-driven insights into market opportunities, competitive positioning, and growth potential within the gaming industry."
            ],
            'casual': [
                "Hey there! 👋 While I'm fine-tuning my responses, I can share that we're discovering some really interesting patterns in how different player demographics engage with games!",
                "Hi! 😊 Our analytics are revealing fascinating insights about gaming trends. Want to know what we're learning about player preferences and behavior patterns?"
            ],
            'anxious': [
                "I'm here to support you. 🤗 Our platform is designed to make complex data accessible and actionable. We break down insights into clear, manageable information.",
                "You're in good hands. 💪 We've built robust systems to ensure you get reliable, valuable insights from our gaming analytics platform."
            ]
        }
        
        response_pool = premium_fallbacks.get(emotion_analysis['primary_emotion'], [
            "I appreciate your message! 💡 I'm currently enhancing my response capabilities to provide you with even more valuable insights about gaming analytics and beyond.",
            "Thank you for reaching out! 🌟 I'm optimizing my systems to deliver premium insights about gaming trends, user behavior, and market opportunities."
        ])
        
        return random.choice(response_pool)
    
    def get_conversation_style(self, user_message: str) -> str:
        """Determine optimal conversation style based on user message"""
        message_lower = user_message.lower()
        
        if any(word in message_lower for word in ['analyze', 'data', 'metrics', 'report', 'numbers', 'statistics']):
            return 'analytical'
        elif any(word in message_lower for word in ['creative', 'innovative', 'idea', 'brainstorm', 'imagine']):
            return 'creative'
        elif any(word in message_lower for word in ['brief', 'quick', 'summary', 'tl;dr', 'short']):
            return 'concise'
        elif any(word in message_lower for word in ['detail', 'explain', 'how does', 'why', 'comprehensive']):
            return 'detailed'
        elif any(word in message_lower for word in ['motivate', 'inspire', 'encourage', 'positive']):
            return 'inspirational'
        else:
            return 'balanced'