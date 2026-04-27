import os
import google.generativeai as genai

API_KEY = "AIzaSyDpR9eQ_x-7aH-7YnFANOlLV9BJryjPV1k"
genai.configure(api_key=API_KEY)

try:
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    response = model.generate_content("Say hello")
    print("SUCCESS!")
    print(response.text)
except Exception as e:
    print("FAILED gemini-1.5-pro-latest:")
    print(str(e))

try:
    model2 = genai.GenerativeModel('gemini-1.5-pro')
    response2 = model2.generate_content("Say hello")
    print("SUCCESS with gemini-1.5-pro!")
    print(response2.text)
except Exception as e:
    print("FAILED gemini-1.5-pro:")
    print(str(e))

try:
    model3 = genai.GenerativeModel('gemini-pro')
    response3 = model3.generate_content("Say hello")
    print("SUCCESS with gemini-pro!")
    print(response3.text)
except Exception as e:
    print("FAILED gemini-pro:")
    print(str(e))
