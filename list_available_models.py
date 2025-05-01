import google.generativeai as genai
import sys

# Usage: python list_available_models.py YOUR_API_KEY
if len(sys.argv) != 2:
    print("Usage: python list_available_models.py YOUR_API_KEY")
    sys.exit(1)

api_key = sys.argv[1]
genai.configure(api_key=api_key)

# List all available models
for model in genai.list_models():
    print(f"Model name: {model.name}")
    print(f"Display name: {model.display_name}")
    print(f"Description: {model.description}")
    print(f"Supported generation methods: {model.supported_generation_methods}")
    print("-" * 50)