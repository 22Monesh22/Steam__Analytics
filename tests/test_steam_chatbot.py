# fixed_steam_chatbot.py
import json
import google.generativeai as genai
import os
import time

class FixedSteamChatbot:
    def __init__(self, api_key: str, meta_file: str = "steam_chatbot_meta.json"):
        self.api_key = api_key
        self.meta_data = self._load_meta(meta_file)
        self._configure_gemini()
        
    def _load_meta(self, meta_file: str):
        """Load the steam games meta data"""
        if not os.path.exists(meta_file):
            raise FileNotFoundError(f"Meta file not found: {meta_file}")
        
        with open(meta_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _configure_gemini(self):
        """Configure Gemini API with correct model names"""
        genai.configure(api_key=self.api_key)
        
        # List available models to see what's available
        try:
            models = genai.list_models()
            print("✅ Available Gemini Models:")
            for model in models:
                if 'generateContent' in model.supported_generation_methods:
                    print(f"   - {model.name}")
        except Exception as e:
            print(f"⚠️ Could not list models: {e}")
        
        # Try different model names
        model_names = [
            "gemini-1.5-pro",  # Newest model
            "gemini-1.0-pro",  # Older but stable
            "gemini-pro",      # Legacy name
            "models/gemini-pro"  # Full path
        ]
        
        self.model = None
        for model_name in model_names:
            try:
                self.model = genai.GenerativeModel(model_name)
                # Test with a simple prompt
                test_response = self.model.generate_content("Say hello")
                print(f"✅ Successfully configured model: {model_name}")
                break
            except Exception as e:
                print(f"❌ Model {model_name} failed: {e}")
                continue
        
        if self.model is None:
            raise Exception("No working Gemini model found. Please check your API key and available models.")
    
    def get_system_context(self):
        """Create comprehensive context about the Steam games dataset"""
        stats = self.meta_data['dataset_stats']
        top_tags = self.meta_data['top_tags'][:15]
        
        context = f"""
        STEAM GAMES ANALYTICS ASSISTANT

        DATASET OVERVIEW:
        - Total Games: {stats['total_games']:,}
        - Unique Tags: {stats['unique_tags']:,}
        - Games with Descriptions: {stats['games_with_descriptions']:,}

        TOP 15 GAME TAGS/GENRES:
        {chr(10).join([f"        - {tag['tag']}: {tag['count']:,} games" for tag in top_tags])}

        YOU ARE AN EXPERT IN:
        1. Game Discovery & Recommendation
        2. Steam Market Analysis
        3. Genre Trends and Insights
        4. Game Development Market Analysis

        Always provide specific, data-driven insights based on the 50,872 games dataset.
        Focus on practical advice for gamers and developers.
        """
        return context
    
    def send_message(self, user_message: str) -> str:
        """Send message with proper error handling and retries"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                context = self.get_system_context()
                prompt = f"{context}\n\nUser Question: {user_message}"
                
                response = self.model.generate_content(prompt)
                return response.text
                
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"⚠️ Attempt {attempt + 1} failed, retrying...")
                    time.sleep(2)  # Wait before retry
                else:
                    return f"I apologize, but I encountered an error: {str(e)}\n\nHowever, based on the Steam dataset analysis, I can tell you that we have analyzed 50,872 games with 441 unique tags. The top genres are Indie, Action, Adventure, and Casual games."

def main():
    API_KEY = "AIzaSyAcO-KsHDV8cRathRRUqyolzc3PkiPQPbE"
    
    print("🎮 STEAM GAMES ANALYTICS CHATBOT (FIXED)")
    print("=" * 60)
    
    try:
        # Initialize chatbot
        chatbot = FixedSteamChatbot(api_key=API_KEY)
        
        print("\n✅ Chatbot initialized successfully!")
        
        # Show dataset information
        stats = chatbot.meta_data['dataset_stats']
        print(f"\n📊 DATASET LOADED:")
        print(f"   Total Games: {stats['total_games']:,}")
        print(f"   Unique Tags: {stats['unique_tags']:,}")
        print(f"   Top Genre: Indie ({chatbot.meta_data['top_tags'][0]['count']:,} games)")
        
        print("\n💬 Starting Steam Games Analysis...")
        print("=" * 60)
        
        # Test questions with fallback responses
        test_questions = [
            "What are the most popular game genres?",
            "Recommend games for someone who likes RPGs",
            "What's the indie game market like?",
            "How many free-to-play games are there?"
        ]
        
        for i, question in enumerate(test_questions, 1):
            print(f"\n{i}. 👤 YOU: {question}")
            print("-" * 50)
            response = chatbot.send_message(question)
            print(f"🤖 ASSISTANT: {response}")
            print("=" * 80)
            
        print("\n🎉 CHATBOT TEST COMPLETED!")
        
    except Exception as e:
        print(f"❌ Initialization Error: {e}")
        print("\n💡 TROUBLESHOOTING:")
        print("1. Check if your API key is valid")
        print("2. Make sure you have internet connection")
        print("3. Try updating the google-generativeai package:")
        print("   pip install --upgrade google-generativeai")
        print("4. Check Google AI Studio for available models")

if __name__ == "__main__":
    main()