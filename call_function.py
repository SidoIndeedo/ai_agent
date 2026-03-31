from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.write_file import schema_write_file, write_file
from functions.run_python_file import schema_run_python_file, run_python_file
from google import genai
from google.genai import types


available_functions = types.Tool(
    function_declarations=[schema_get_files_info, schema_get_file_content, 
    schema_write_file, schema_run_python_file],
)

# Mapping of function names to implementations
function_implementations = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file,
}

def call_function(function_call, working_directory="./calculator", verbose=False):
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