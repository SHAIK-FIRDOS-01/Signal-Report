import os
import google.generativeai as genai

API_KEY = "AIzaSyB10_oepH50YxnAUnO8iKD9Q1Bq9a3Qp4o"
genai.configure(api_key=API_KEY)

# Try 2.5-flash
try:
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content("Say hello")
    print("SUCCESS with gemini-2.5-flash!")
    print(response.text)
except Exception as e:
    print("FAILED gemini-2.5-flash:")
    print(str(e))

# Try 2.0-flash
try:
    model2 = genai.GenerativeModel('gemini-2.0-flash')
    response2 = model2.generate_content("Say hello")
    print("SUCCESS with gemini-2.0-flash!")
    print(response2.text)
except Exception as e:
    print("FAILED gemini-2.0-flash:")
    print(str(e))
