from dotenv import load_dotenv
import os
from groq import Groq

# Load API keys from .env file
load_dotenv()

# Get the Groq API key
groq_api_key = os.getenv("GROQ_API_KEY")

# Check if key exists
if not groq_api_key:
    print("❌ ERROR: Groq API key not found in .env file!")
    print("Please add: GROQ_API_KEY=your_key_here")
    exit()

# Initialize Groq client
client = Groq(api_key=groq_api_key)

print("\n🤖 Welcome to Your AI Assistant!")
print("Type 'quit' to exit\n")

# Chat loop - keeps the conversation going
while True:
    # Get user input
    user_input = input("You: ")

    # Check if user wants to quit
    if user_input.lower() in ['quit', 'exit', 'q']:
        print("Goodbye! 👋")
        break

    # Get AI response
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # ✅ UPDATED - WORKING MODEL
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant. Answer in a clear and friendly way."},
                {"role": "user", "content": user_input}
            ]
        )

        # Print the response
        ai_response = response.choices[0].message.content
        print(f"\n🤖 AI: {ai_response}\n")

    except Exception as e:
        print(f"❌ Error: {e}")
