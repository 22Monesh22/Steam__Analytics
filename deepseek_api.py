import requests
import json
import sys

def ask_deepseek(question, api_key="sk-4dc7764573d84f9892e30f94f41c007c"):
    url = "https://api.deepseek.com/v1/chat/completions"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    data = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": question}],
        "stream": False,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        result = response.json()
        return result['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"
    except KeyError:
        return "Error: Unexpected response format"
    except json.JSONDecodeError:
        return "Error: Invalid JSON response"

def interactive_chat():
    print("DeepSeek Chat - Type 'quit' or 'exit' to end")
    print("-" * 50)
    
    while True:
        question = input("\nYou: ").strip()
        
        if question.lower() in ['quit', 'exit', 'bye']:
            print("Goodbye!")
            break
            
        if not question:
            continue
            
        print("DeepSeek: ", end="", flush=True)
        answer = ask_deepseek(question)
        print(answer)

# Test it
if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Command line mode: python deepseek_api.py "Your question"
        question = " ".join(sys.argv[1:])
        answer = ask_deepseek(question)
        print(answer)
    else:
        # Interactive mode
        interactive_chat()