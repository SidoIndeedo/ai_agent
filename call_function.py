from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.write_file import schema_write_file, write_file
from functions.run_python_file import schema_run_python_file, run_python_file
from google import genai
from google.genai import types


# available_functions = types.Tool(
#     function_declarations=[schema_get_files_info, schema_get_file_content, 
#     schema_write_file, schema_run_python_file],
# )

# Mapping of function names to implementations
function_implementations = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file,
}

available_functions_list = [
    {
        'type': 'function',
        'function': {
            'name': 'get_files_info',
            'description': 'Lists files in a directory relative to the working directory',
            'parameters': {
                'type': 'object',
                'properties': {
                    'directory': {'type': 'string', 'description': 'The relative directory path'}
                },
                'required': ['directory'],
            },
        },
    },
    {
        'type': 'function',
        'function': {
            'name': 'get_file_content',
            'description': 'Reads the content of a specific file',
            'parameters': {
                'type': 'object',
                'properties': {
                    'file_path': {'type': 'string', 'description': 'The relative file path'}
                },
                'required': ['file_path'],
            },
        },
    },
    {
        'type': 'function',
        'function': {
            'name': 'write_file',
            'description': 'Writes content to a file, overwriting if it exists',
            'parameters': {
                'type': 'object',
                'properties': {
                    'file_path': {'type': 'string', 'description': 'The relative file path'},
                    'content': {'type': 'string', 'description': 'The text content to write'}
                },
                'required': ['file_path', 'content'],
            },
        },
    },
    {
        'type': 'function',
        'function': {
            'name': 'run_python_file',
            'description': 'Executes a Python file and returns the output',
            'parameters': {
                'type': 'object',
                'properties': {
                    'file_path': {'type': 'string', 'description': 'The relative path of the .py file'},
                    'args': {
                        'type': 'array', 
                        'items': {'type': 'string'}, 
                        'description': 'Optional arguments list'
                    }
                },
                'required': ['file_path'],
            },
        },
    }
]

def better_call_function(function_call, working_directory="./calculator", verbose=False):
    function_name = function_call.name or ""

    if verbose:
        print(f"Function call requested: {function_name} with args: {function_call.args}")
    else:
        print(f"Function call requested: {function_name}")

    if function_name not in function_implementations:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    args = dict(function_call.args) if function_call.args else {}
    args["working_directory"] = working_directory

    function_to_call = function_implementations[function_name]
    function_result = function_to_call(**args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ]
    )