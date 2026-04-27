import os
import google.generativeai as genai

API_KEY = "AIzaSyDpR9eQ_x-7aH-7YnFANOlLV9BJryjPV1k"
genai.configure(api_key=API_KEY)

for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)
