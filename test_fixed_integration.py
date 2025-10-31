# test_fixed_integration.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.services.dashboard_ai_agent import DashboardAIAgent

def test_fixed_integration():
    print("🧪 Testing Fixed AI Engine Integration...")
    
    agent = DashboardAIAgent()
    
    # Test different types of messages
    test_messages = [
        "hi",
        "What does this dashboard show?",
        "Show me user metrics",
        "What are the trends?",
        "Explain the data"
    ]
    
    for message in test_messages:
        print(f"\n{'='*50}")
        print(f"Testing: '{message}'")
        print(f"{'='*50}")
        
        result = agent.process_message(
            message,
            "http://127.0.0.1:5000/powerbi/dashboard/user-analytics"
        )
        
        print(f"✅ Success: {result['success']}")
        print(f"🤖 Uses AI Engine: {result.get('uses_ai_engine', False)}")
        print(f"📝 Response Preview: {result['response'][:150]}...")
        print(f"💡 Suggestions: {result['suggestions'][:2]}...")

if __name__ == "__main__":
    test_fixed_integration()