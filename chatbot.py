# import os
# from openai import OpenAI
# from config import OPENAI_API_KEY, DEFAULT_MODEL

# # Load system prompt
# with open("prompts/system_prompt.txt", "r", encoding="utf-8") as f:
#     SYSTEM_PROMPT = f.read()

# # Initialize OpenAI client
# client = OpenAI(api_key=OPENAI_API_KEY)

# # Conversation history for context
# conversation_history = [
#     {"role": "system", "content": SYSTEM_PROMPT}
# ]

# def chat_with_child(user_input: str) -> str:
#     """Send child's message to the LLM and get a therapeutic reply."""
#     conversation_history.append({"role": "user", "content": user_input})

#     response = client.chat.completions.create(
#         model=DEFAULT_MODEL,
#         messages=conversation_history,
#         temperature=0.3
#     )

#     assistant_reply = response.choices[0].message.content.strip()
#     conversation_history.append({"role": "assistant", "content": assistant_reply})

#     return assistant_reply

# if __name__ == "__main__":
#     print("Therapeutic Assistant ready. Type 'quit' to exit.\n")
#     while True:
#         child_message = input("Child: ").strip()
#         if child_message.lower() == "quit":
#             print("Session ended.")
#             break

#         reply = chat_with_child(child_message)
#         print("Assistant:", reply, "\n")


from openai import OpenAI
from config import OPENAI_API_KEY, DEFAULT_MODEL

# Load system prompt
with open("prompts/system_prompt.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Conversation history for context
conversation_history = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

def chat_with_child(user_input: str) -> str:
    """Send child's message to the LLM and get a therapeutic reply."""
    conversation_history.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=conversation_history,
        temperature=0.3
    )

    assistant_reply = response.choices[0].message.content.strip()
    conversation_history.append({"role": "assistant", "content": assistant_reply})

    return assistant_reply
