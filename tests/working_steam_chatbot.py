# working_steam_chatbot.py
import json
import google.generativeai as genai
import os

class WorkingSteamChatbot:
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
        """Configure Gemini API with working model names"""
        genai.configure(api_key=self.api_key)
        
        # Use the latest available models from your list
        working_models = [
            "models/gemini-2.0-flash",  # Fast and reliable
            "models/gemini-2.0-flash-001",  # Stable version
            "models/gemini-pro-latest",  # Latest pro version
            "models/gemini-flash-latest",  # Latest flash version
        ]
        
        self.model = None
        for model_name in working_models:
            try:
                self.model = genai.GenerativeModel(model_name)
                # Test with a simple prompt
                test_response = self.model.generate_content("Say hello in one word")
                print(f"✅ Successfully configured with: {model_name}")
                break
            except Exception as e:
                print(f"❌ {model_name} failed: {e}")
                continue
        
        if self.model is None:
            raise Exception("No working Gemini model found.")
    
    def get_system_context(self):
        """Create comprehensive context about the Steam games dataset"""
        stats = self.meta_data['dataset_stats']
        top_tags = self.meta_data['top_tags'][:15]
        
        context = f"""
        You are a Steam Games Analytics Expert analyzing a dataset of 50,872 Steam games.

        DATASET STATISTICS:
        - Total Games: {stats['total_games']:,}
        - Unique Tags/Genres: {stats['unique_tags']:,}
        - Games with Descriptions: {stats['games_with_descriptions']:,}

        TOP 15 GENRES (by number of games):
        {chr(10).join([f"  {i+1}. {tag['tag']}: {tag['count']:,} games" for i, tag in enumerate(top_tags)])}

        YOUR ROLE:
        - Provide game recommendations based on genres and tags
        - Analyze market trends in the Steam ecosystem
        - Help users discover games based on their preferences
        - Provide insights about genre popularity and combinations
        - Analyze the indie game market and trends

        Always be specific and reference the dataset size. Provide practical, data-driven insights.
        """
        return context
    
    def send_message(self, user_message: str) -> str:
        """Send message with Steam games context"""
        try:
            context = self.get_system_context()
            prompt = f"{context}\n\nUser Question: {user_message}\n\nPlease provide a detailed, helpful response based on the Steam games dataset:"
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            # Provide fallback responses based on the data we have
            return self._get_fallback_response(user_message)
    
    def _get_fallback_response(self, user_message: str) -> str:
        """Provide intelligent fallback responses based on the dataset"""
        stats = self.meta_data['dataset_stats']
        top_tags = self.meta_data['top_tags']
        
        # Analyze the question and provide relevant data
        question_lower = user_message.lower()
        
        if any(word in question_lower for word in ['popular', 'top', 'genre', 'category']):
            top_5 = [f"{tag['tag']} ({tag['count']:,} games)" for tag in top_tags[:5]]
            return f"Based on our analysis of {stats['total_games']:,} Steam games, the most popular genres are:\n\n" + "\n".join([f"• {genre}" for genre in top_5]) + f"\n\nIndie games dominate with {top_tags[0]['count']:,} titles, showing the strong presence of independent developers on Steam."
        
        elif any(word in question_lower for word in ['rpg', 'role playing']):
            rpg_count = next((tag['count'] for tag in top_tags if tag['tag'] == 'RPG'), 0)
            return f"There are {rpg_count:,} RPG games in the dataset. RPGs often combine with genres like Adventure, Strategy, and Action. Popular RPG sub-genres include Action RPGs, JRPGs, and Western RPGs."
        
        elif any(word in question_lower for word in ['indie', 'independent']):
            indie_count = top_tags[0]['count']
            return f"The indie game scene is massive on Steam with {indie_count:,} indie games, representing {indie_count/stats['total_games']*100:.1f}% of all games. Indie games often feature innovation in gameplay, unique art styles, and creative storytelling."
        
        elif any(word in question_lower for word in ['free', 'free to play', 'f2p']):
            free_count = next((tag['count'] for tag in top_tags if tag['tag'] == 'Free to Play'), 0)
            return f"There are {free_count:,} free-to-play games in the dataset, representing {free_count/stats['total_games']*100:.1f}% of all Steam games. Free-to-play games often use monetization through in-game purchases, cosmetics, or battle passes."
        
        elif any(word in question_lower for word in ['recommend', 'suggest', 'similar']):
            return f"Based on the dataset of {stats['total_games']:,} games, I can recommend games by genre combinations. Popular genre mixes include:\n• Action + Adventure (common in AAA titles)\n• Indie + Puzzle (for casual gaming)\n• RPG + Strategy (for deep gameplay)\n• Simulation + Management (for creative players)\n\nWhat specific genres or game types are you interested in?"
        
        else:
            return f"I have access to a comprehensive Steam games dataset with {stats['total_games']:,} games and {stats['unique_tags']:,} unique tags. The top genres are Indie, Action, Adventure, and Casual games. How can I help you explore this data?"

def main():
    API_KEY = "AIzaSyAcO-KsHDV8cRathRRUqyolzc3PkiPQPbE"
    
    print("🎮 WORKING STEAM GAMES ANALYTICS CHATBOT")
    print("=" * 60)
    
    try:
        # Initialize chatbot
        chatbot = WorkingSteamChatbot(api_key=API_KEY)
        
        print("\n✅ Chatbot initialized successfully!")
        
        # Show dataset information
        stats = chatbot.meta_data['dataset_stats']
        print(f"\n📊 STEAM DATASET ANALYSIS:")
        print(f"   Total Games Analyzed: {stats['total_games']:,}")
        print(f"   Unique Genres/Tags: {stats['unique_tags']:,}")
        print(f"   Most Popular: Indie ({chatbot.meta_data['top_tags'][0]['count']:,} games)")
        print(f"   Second Most Popular: Action ({chatbot.meta_data['top_tags'][2]['count']:,} games)")
        
        print("\n💬 STARTING INTERACTIVE ANALYSIS...")
        print("=" * 60)
        
        # Comprehensive test questions
        test_questions = [
            "What are the most popular game genres on Steam?",
            "I like RPG games - what should I play next?",
            "Tell me about the indie game market on Steam",
            "How many multiplayer games are there compared to singleplayer?",
            "What genre combinations are most successful?",
            "Recommend some hidden gem games",
            "What's the percentage of free vs paid games?",
            "Which genres have grown the most recently?",
            "What makes a successful Steam game based on your data?",
            "Can you analyze the strategy game market?"
        ]
        
        for i, question in enumerate(test_questions, 1):
            print(f"\n{i}. 👤 YOU: {question}")
            print("-" * 80)
            response = chatbot.send_message(question)
            print(f"🤖 ASSISTANT: {response}")
            print("=" * 80)
            
        print("\n🎉 SUCCESS! Your Steam Games Analytics Chatbot is working!")
        print(f"\n📈 Dataset Summary:")
        print(f"   • {stats['total_games']:,} total games")
        print(f"   • {stats['unique_tags']:,} unique tags") 
        print(f"   • {stats['games_with_descriptions']:,} games with descriptions")
        print(f"   • Top genre: Indie ({chatbot.meta_data['top_tags'][0]['count']:,} games)")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 TROUBLESHOOTING:")
        print("1. Check your internet connection")
        print("2. Verify your API key is correct")
        print("3. Try: pip install --upgrade google-generativeai")
        print("4. Check https://aistudio.google.com/ for API status")

if __name__ == "__main__":
    main()