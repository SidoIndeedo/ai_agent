import os
import requests
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key=os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)
# user_prompt = 'Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.'

# def ask_llama(prompt):
#     res = requests.post()

def main():
    print("hello")

parser = argparse.ArgumentParser(description="what do you need?")
parser.add_argument("user_prompt", type=str, help="user prompt")
parser.add_argument("--verbose", action="store_true", help="enable verbose output")
args = parser.parse_args()
user_prompt = args.user_prompt
messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]


response = client.models.generate_content(
    model='gemini-2.5-flash-lite', contents=messages
)



prompt_tokens = response.usage_metadata.prompt_token_count
candidate_tokens = response.usage_metadata.candidates_token_count

if args.verbose:

    if response.usage_metadata is None:
        raise RuntimeError("API req failed")

    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {candidate_tokens}")
print(response.text)


# print(f"user prompt: {user_prompt}")

# print("Response:")
# print(response.text)


if __name__ == "__main__":
    main()
