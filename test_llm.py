import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
# Note: If using OpenAI instead, uncomment the line below:
# from langchain_openai import ChatOpenAI

# 1. Load API keys from .env file
load_dotenv()

# 2. Initialize the LLM
    llm = ChatGoogleGenerativeAI(
        model=os.getenv("LLM_MODEL", "gemini-3.5-flash"),
        google_api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0.1
    )

# 3. Test LLM call
response = llm.invoke("You are a legal AI assistant. Explain in 1 sentence what an NDA (Non-Disclosure Agreement) is.")
print("\n--- LLM Response ---")
print(response.content)