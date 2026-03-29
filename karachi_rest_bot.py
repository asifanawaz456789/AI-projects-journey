"""
Karachi Darbar Restaurant Chatbot
A terminal-based AI assistant using Groq API
"""

import requests
from typing import List, Dict

# ============================================
# CONFIGURATION
# ============================================

API_KEY = "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"
API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.1-8b-instant"
MAX_TOKENS = 512

# ============================================
# RESTAURANT DATA
# ============================================

RESTAURANT_INFO = {
    "name": "Karachi Darbar",
    "timing": "12pm - 12am",
    "location": "Karachi, Saddar",
    "phone": "021-1234567",
    "menu": {
        "Biryani": 500,
        "Nihari": 400,
        "Karahi": 800,
        "Naan": 50
    }
}

# ============================================
# SYSTEM PROMPT
# ============================================

SYSTEM_PROMPT = f"""
You are a helpful chatbot for {RESTAURANT_INFO['name']}.

📋 MENU:
- Biryani = {RESTAURANT_INFO['menu']['Biryani']} Rs
- Nihari = {RESTAURANT_INFO['menu']['Nihari']} Rs
- Karahi = {RESTAURANT_INFO['menu']['Karahi']} Rs
- Naan = {RESTAURANT_INFO['menu']['Naan']} Rs

⏰ Timing: {RESTAURANT_INFO['timing']}
📍 Location: {RESTAURANT_INFO['location']}
📞 Table Booking: {RESTAURANT_INFO['phone']}

RULES:
1. Only answer questions related to {RESTAURANT_INFO['name']}
2. Help customers with menu, prices, table booking, location, and timing
3. If someone asks anything unrelated, reply exactly:
   "I can only help you with Karachi Darbar related queries!"
"""

# ============================================
# CHATBOT CLASS
# ============================================

class KarachiDarbarBot:
    """Restaurant chatbot using Groq API"""
    
    def __init__(self):
        self.messages: List[Dict[str, str]] = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]
    
    def get_response(self, user_input: str) -> str:
        """
        Send user message to API and get bot response
        """
        # Add user message to history
        self.messages.append({"role": "user", "content": user_input})
        
        # Prepare API request
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "model": MODEL,
            "messages": self.messages,
            "max_tokens": MAX_TOKENS,
            "temperature": 0.7  # Added for better responses
        }
        
        try:
            # Make API call
            response = requests.post(API_URL, json=payload, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                reply = data["choices"][0]["message"]["content"]
                
                # Save AI reply to history
                self.messages.append({"role": "assistant", "content": reply})
                return reply
            else:
                return f"❌ API Error: {response.status_code}\n{response.text}"
                
        except requests.exceptions.ConnectionError:
            return "❌ Connection Error: Please check your internet connection!"
        except Exception as e:
            return f"❌ Unexpected Error: {str(e)}"
    
    def clear_history(self):
        """Clear conversation history (keep system prompt)"""
        self.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        print("✅ Conversation history cleared!")
    
    def show_help(self):
        """Display help information"""
        help_text = """
╔══════════════════════════════════════════════════════╗
║                    HELP MENU                         ║
╠══════════════════════════════════════════════════════╣
║  • Ask about menu items and prices                   ║
║  • Check restaurant timings                          ║
║  • Get location details                              ║
║  • Book a table (provides phone number)              ║
║                                                      ║
║  COMMANDS:                                           ║
║    help     - Show this menu                         ║
║    clear    - Clear conversation history             ║
║    exit     - Exit the chatbot                       ║
╚══════════════════════════════════════════════════════╝
        """
        print(help_text)

# ============================================
# MAIN FUNCTION
# ============================================

def main():
    """Main chatbot loop"""
    
    # Welcome message
    print("\n" + "="*60)
    print("🍛 WELCOME TO KARACHI DARBAR CHATBOT 🍛")
    print("="*60)
    print(f"📍 {RESTAURANT_INFO['location']}")
    print(f"⏰ {RESTAURANT_INFO['timing']}")
    print("="*60)
    print("Type 'help' for commands, 'exit' to quit\n")
    
    # Initialize bot
    bot = KarachiDarbarBot()
    
    # Main conversation loop
    while True:
        try:
            # Get user input
            user_input = input("🍽️ You: ").strip()
            
            # Check for empty input
            if not user_input:
                continue
            
            # Handle commands
            if user_input.lower() == "exit":
                print("\n👋 Thank you for visiting Karachi Darbar! Goodbye!\n")
                break
            elif user_input.lower() == "help":
                bot.show_help()
                continue
            elif user_input.lower() == "clear":
                bot.clear_history()
                continue
            
            # Get and display bot response
            print("🤖 AI: ", end="")
            response = bot.get_response(user_input)
            print(response + "\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Come again!\n")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}\n")

# ============================================
# RUN THE BOT
# ============================================

if __name__ == "__main__":
    main()