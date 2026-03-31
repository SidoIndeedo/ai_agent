import os
import argparse
import ollama  # Make sure to pip install ollama
from prompt import system_prompt
# Import the list and the map we created
from call_function import available_functions_list, function_implementations

parser = argparse.ArgumentParser(description="Local AI Agent")
parser.add_argument("user_prompt", type=str, help="User prompt to send to the AI agent")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

def main():
    # Include the system prompt in the messages history immediately
    messages = [
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': args.user_prompt}
    ]

    for i in range(20):
        if args.verbose:
            print(f"\n-- Iteration {i+1} --")

        response = ollama.chat(
            model='llama3.1', # Ensure you have run 'ollama pull llama3.1'
            messages=messages,
            tools=available_functions_list,
        )

        # 1. Save the model's message (which might contain tool_calls)
        messages.append(response['message'])

        # 2. Check if we are done (no tool calls)
        if not response['message'].get('tool_calls'):
            print('\nFinal response:')
            print(response['message']['content'])
            break

        # 3. Handle Tool Calls
        for tool in response['message'].get('tool_calls', []):
            func_name = tool['function']['name']
            func_args = tool['function']['arguments']

            if args.verbose:
                print(f'Llama wants to call: {func_name}({func_args})')

            # Inject the sandbox path
            func_args['working_directory'] = './calculator'

            # Execute directly from our map
            if func_name in function_implementations:
                actual_func = function_implementations[func_name]
                result = actual_func(**func_args)
            else:
                result = f"Error: Function {func_name} not found."

            # 4. Add the tool RESULT back to history
            # Note: For Llama, the role is 'tool'
            messages.append({
                'role': 'tool',
                'content': str(result),
            })
    else:
        print('Error: max iteration reached')

if __name__ == "__main__":
    main()