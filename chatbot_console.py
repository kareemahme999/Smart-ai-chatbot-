import os

from dotenv import load_dotenv

from core.chatbot_engine import ChatbotError, SmartChatbot


def main() -> None:
    load_dotenv()
    print("=== 🤖 Smart AI Chatbot (Console) ===")
    print("TechMaster Academy · Phase 04 / Project 04")
    print("Type 'exit' to quit or 'reset' to clear the conversation.\n")

    api_key = os.getenv("COHERE_API_KEY")
    try:
        bot = SmartChatbot(api_key=api_key)
    except ChatbotError as e:
        print(f"❌ Error: {e}")
        return

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        if user_input.lower() == "reset":
            bot.reset_conversation()
            print("(Conversation context cleared)\n")
            continue

        try:
            reply = bot.send_message(user_input)
            print(f"Bot: {reply}\n")
        except ChatbotError as e:
            print(f"❌ Error: {e}\n")


if __name__ == "__main__":
    main()
