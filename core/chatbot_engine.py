import os
import time
from typing import Dict, List, Optional

import cohere


class ChatbotError(Exception):
    pass


class SmartChatbot:
    DEFAULT_SYSTEM_PROMPT = (
        "You are Smart AI Chatbot, a helpful and friendly assistant built for the "
        "TechMaster Academy project. Keep answers clear, accurate, and concise. "
        "If you are not sure about something, say so honestly."
    )

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "command-r",
        system_prompt: Optional[str] = None,
    ):
        self.api_key = api_key or os.getenv("COHERE_API_KEY")
        if not self.api_key:
            raise ChatbotError(
                "Cohere API key not found. Add COHERE_API_KEY to your .env file "
                "or enter it manually."
            )

        try:
            self.client = cohere.Client(self.api_key)
        except Exception as e:
            raise ChatbotError(f"Could not create a connection to the API: {e}") from e

        self.model = model
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT

        self.conversation_history: List[Dict[str, str]] = []

    def _build_chat_history(self) -> List[Dict[str, str]]:
        history = []
        for turn in self.conversation_history:
            role = "USER" if turn["role"] == "user" else "CHATBOT"
            history.append({"role": role, "message": turn["content"]})
        return history

    def send_message(self, user_message: str, max_retries: int = 2) -> str:
        if not user_message or not user_message.strip():
            raise ChatbotError("Message is empty. Please type your question first.")

        chat_history = self._build_chat_history()
        attempt = 0
        last_error: Optional[Exception] = None

        while attempt <= max_retries:
            try:
                response = self.client.chat(
                    message=user_message,
                    model=self.model,
                    preamble=self.system_prompt,
                    chat_history=chat_history,
                    temperature=0.5,
                )
                reply = (response.text or "").strip()
                if not reply:
                    raise ChatbotError("The model returned no reply. Try rephrasing your question.")

                self.conversation_history.append({"role": "user", "content": user_message})
                self.conversation_history.append({"role": "assistant", "content": reply})
                return reply

            except cohere.errors.UnauthorizedError as e:
                raise ChatbotError("Invalid or expired API key. Please check it and try again.") from e

            except cohere.errors.TooManyRequestsError as e:
                last_error = e
                attempt += 1
                time.sleep(1.5 * attempt)

            except cohere.errors.CohereError as e:
                last_error = e
                attempt += 1
                time.sleep(1)

            except Exception as e:
                last_error = e
                attempt += 1
                time.sleep(1)

        raise ChatbotError(f"Failed to reach the AI API after several attempts. Details: {last_error}")

    def reset_conversation(self) -> None:
        self.conversation_history = []

    def get_history(self) -> List[Dict[str, str]]:
        return self.conversation_history
