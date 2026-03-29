"""
StyleZone PK - Online Clothing Shop Chatbot
A professional AI assistant for customer support
"""

import requests
import sys
from typing import List, Dict, Optional

# ============================================
# CONFIGURATION
# ============================================

API_URL = "https://api.groq.com/openai/v1/chat/completions"
API_KEY = "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"
MODEL = "llama-3.1-8b-instant"
MAX_TOKENS = 200
MAX_HISTORY = 6  # Keep last 6 messages for context

# ============================================
# SHOP INFORMATION
# ============================================

SHOP_INFO = {
    "name": "StyleZone PK",
    "location": "Lahore",
    "whatsapp": "0300-1234567",
    "delivery_days": "3-5 working days",
    "products": {
        "Lawn Suit": 2500,
        "Linen Shirt": 1800,
        "Jeans": 3000,
        "Kurta": 1500
    }
}

# ============================================
# SYSTEM PROMPT
# ============================================

SYSTEM_PROMPT = f"""
You are the helpful assistant for {SHOP_INFO['name']}, an online clothing shop.

🏪 Shop Info:
Naam: {SHOP_INFO['name']}
📍 Location: {SHOP_INFO['location']}
📞 WhatsApp: {SHOP_INFO['whatsapp']}
🚚 Delivery: {SHOP_INFO['delivery_days']}

👕 Products & Prices:
- Lawn Suit = {SHOP_INFO['products']['Lawn Suit']} Rs
- Linen Shirt = {SHOP_INFO['products']['Linen Shirt']} Rs
- Jeans = {SHOP_INFO['products']['Jeans']} Rs
- Kurta = {SHOP_INFO['products']['Kurta']} Rs

📋 Rules:
- Only answer questions related to {SHOP_INFO['name']} shop, its products, pricing, delivery, location, or contact details.
- If someone asks anything unrelated, reply exactly:
'Main sirf StyleZone PK shop ke baare mein madad kar sakta hoon!'
- Be helpful, friendly, and professional in Urdu or English as the customer prefers.
"""

# ============================================
# CHATBOT CLASS
# ============================================

class StyleZoneBot:
    """Professional chatbot for StyleZone PK"""
    
    def __init__(self):
        self.messages: List[Dict[str, str]] = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]
        self.conversation_count = 0
    
    def get_response(self, user_input: str) -> Optional[str]:
        """
        Get AI response for user message
        """
        # Add user message to history
        self.messages.append({"role": "user", "content": user_input})
        self.conversation_count += 1
        
        # Prepare API request
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": MODEL,
            "messages": self.messages[-MAX_HISTORY:],  # Keep only recent history
            "max_tokens": MAX_TOKENS,
            "temperature": 0.7  # Balanced responses
        }
        
        try:
            # Make API call
            response = requests.post(API_URL, json=payload, headers=headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                reply = data["choices"][0]["message"]["content"]
                
                # Add AI reply to history
                self.messages.append({"role": "assistant", "content": reply})
                return reply
            else:
                return f"❌ Server Error: {response.status_code}\nPlease try again later."
                
        except requests.exceptions.Timeout:
            return "⏰ Request timeout! Please try again."
        except requests.exceptions.ConnectionError:
            return "🌐 Connection Error! Please check your internet."
        except Exception as e:
            return f"⚠️ Error: {str(e)}"
    
    def clear_history(self):
        """Reset conversation history"""
        self.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        self.conversation_count = 0
        return "✅ Conversation history cleared!"
    
    def get_stats(self) -> str:
        """Get conversation statistics"""
        return f"""
📊 Conversation Stats:
• Total messages: {len(self.messages)}
• User messages: {self.conversation_count}
• AI responses: {len(self.messages) - self.conversation_count - 1}
        """

# ============================================
# UI HELPERS
# ============================================

def print_banner():
    """Display welcome banner"""
    banner = f"""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║   👕 STYLEZONE PK - ONLINE CLOTHING SHOP 👖              ║
║                                                          ║
║   📍 {SHOP_INFO['location']}              📞 {SHOP_INFO['whatsapp']}   ║
║   🚚 Delivery: {SHOP_INFO['delivery_days']}                        ║
║                                                          ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║   🛍️  PRODUCTS & PRICES:                                 ║
"""
    
    for product, price in SHOP_INFO['products'].items():
        banner += f"║      • {product:<18} = {price:>6} Rs                         ║\n"
    
    banner += f"""║                                                          ║
╠══════════════════════════════════════════════════════════╣
║  💬 Commands:                                            ║
║     help   - Show this menu                              ║
║     clear  - Reset conversation                          ║
║     stats  - Show conversation stats                     ║
║     exit   - Quit chatbot                                ║
║                                                          ║
║  💡 Tip: Ask in Urdu or English!                         ║
╚══════════════════════════════════════════════════════════╝
"""
    print(banner)

def print_help():
    """Display help menu"""
    help_text = """
╔════════════════════════════════════════════╗
║              💬 HELP MENU                  ║
╠════════════════════════════════════════════╣
║  You can ask about:                        ║
║  • Product prices (Lawn Suit, Jeans etc)   ║
║  • Delivery time and location              ║
║  • WhatsApp contact                        ║
║  • Product quality and size                ║
║  • Return policy                           ║
║                                            ║
║  Commands:                                 ║
║    help   - Show this menu                 ║
║    clear  - Clear chat history             ║
║    stats  - Show conversation stats        ║
║    exit   - Exit chatbot                   ║
╚════════════════════════════════════════════╝
    """
    print(help_text)

# ============================================
# MAIN FUNCTION
# ============================================

def main():
    """Main chatbot loop"""
    
    # Display welcome banner
    print_banner()
    
    # Initialize bot
    bot = StyleZoneBot()
    
    print("🤖 StyleZone PK Assistant: Assalam-o-Alaikum! Main aapki madad kar sakta hoon.\n")
    
    # Main conversation loop
    while True:
        try:
            # Get user input
            user_input = input("👤 You: ").strip()
            
            # Check for empty input
            if not user_input:
                continue
            
            # Handle commands
            cmd = user_input.lower()
            
            if cmd == "exit":
                print("\n👋 StyleZone PK: Shukriya! Phir milenge! 👋\n")
                sys.exit(0)
                
            elif cmd == "help":
                print_help()
                continue
                
            elif cmd == "clear":
                result = bot.clear_history()
                print(f"🤖 StyleZone PK: {result}\n")
                continue
                
            elif cmd == "stats":
                print(bot.get_stats())
                continue
            
            # Get AI response
            print("🤖 StyleZone PK: ", end="")
            response = bot.get_response(user_input)
            print(response + "\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 StyleZone PK: Aapke sawaalon ka shukriya! Khuda Hafiz! 👋\n")
            break
        except Exception as e:
            print(f"⚠️ Unexpected error: {str(e)}\n")

# ============================================
# RUN THE BOT
# ============================================

if __name__ == "__main__":
    main()