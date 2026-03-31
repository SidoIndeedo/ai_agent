import os
import requests
import argparse
from prompt import system_prompt
from call_function import available_functions, call_function
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
    print("")

parser = argparse.ArgumentParser(description="what do you need?")
parser.add_argument("user_prompt", type=str, help="user prompt")
parser.add_argument("--verbose", action="store_true", help="enable verbose output")
args = parser.parse_args()
user_prompt = args.user_prompt
messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]


response = client.models.generate_content(
    model='gemini-2.5-flash', contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
)



prompt_tokens = response.usage_metadata.prompt_token_count
candidate_tokens = response.usage_metadata.candidates_token_count

if args.verbose:

    if response.usage_metadata is None:
        raise RuntimeError("API req failed")

    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {candidate_tokens}")

candidate = response.candidates[0]
if response.function_calls:
    function_results = []

    for function_call in response.function_calls:
        # This matches the specific format requested by your assignment
        print(f"Calling function: {function_call.name}({function_call.args})")
        function_call_result = call_function(function_call, verbose=args.verbose)

        if not function_call_result.parts:
            raise RuntimeError(f"Function call result part list is empty")
        
        part = function_call_result.parts[0]
        if part.function_response is None:
            raise RuntimeError("function_response is None")
        
        if part.function_response.response is None:
            raise RuntimeError("function_response.response is None")

        function_results.append(part)

        if args.verbose:
            print(f"-> {part.function_response.response}")
else:
    # If no function calls, print the text as normal
    print(response.text)





# print(f"user prompt: {user_prompt}")

# print("Response:")
# print(response.text)


if __name__ == "__main__":
    main()
