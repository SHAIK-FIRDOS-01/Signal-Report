import os
import google.generativeai as genai

API_KEY = "AIzaSyDpR9eQ_x-7aH-7YnFANOlLV9BJryjPV1k"
genai.configure(api_key=API_KEY)

try:
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content("Say hello")
    print("SUCCESS with gemini-2.0-flash!")
    print(response.text)
except Exception as e:
    print("FAILED gemini-3.1-pro-preview:")
    print(str(e))
    import traceback
    traceback.print_exc()
