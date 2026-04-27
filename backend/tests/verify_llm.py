import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')
print(f"Using API Key: {api_key[:5]}...{api_key[-5:]}")
genai.configure(api_key=api_key)

try:
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content("Say hello")
    print("SUCCESS with gemini-1.5-flash!")
    print(response.text)
except Exception as e:
    print("FAILED:")
    print(str(e))
