# Import the official Groq client library
from groq import Groq
# Import our settings to securely access the GROQ API key
from config.settings import settings

# Initialize the Groq client with our API key
client = Groq(api_key=settings.GROQ_API_KEY)

# Define a function that takes a question and optional conversation history, returns an answer
def get_llm_response(question: str, history: list = None) -> str:
    try:
        # Build the messages array: start with a system prompt for context
        messages = [
            {
                "role": "system",
                "content": "You are a helpful AI assistant. When the user asks you to shorten, expand, rephrase, or modify your previous answer, do so based on the conversation history provided."
            }
        ]

        # Append past Q&A pairs as alternating user/assistant messages so the model has context
        if history:
            for pair in history:
                messages.append({"role": "user",      "content": pair["question"]})
                messages.append({"role": "assistant", "content": pair["answer"]})

        # Append the current user question
        messages.append({"role": "user", "content": question})

        # Call the Groq chat completions API
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages
        )
        # Extract and return only the text content from the AI's response
        return response.choices[0].message.content
    except Exception as e:
        # If something goes wrong (like a bad API key or no internet), print the error
        print(f"Error calling Groq API: {e}")
        # Return a fallback message so the frontend doesn't crash completely
        return "I'm sorry, I am currently unavailable."
