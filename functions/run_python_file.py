import os
import subprocess
from google import genai
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a specified Python file within the working directory and returns the output (STDOUT and STDERR).",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path of the Python file to execute (e.g., 'main.py' or 'tests.py').",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="An optional list of command-line arguments to pass to the script (e.g., ['3 + 5'] for a calculator).",
            ),
        },
        required=["file_path"],
    ),
)

def run_python_file(working_directory, file_path, args=None):
    try:
        # 1. Path Safety & Normalization
        working_dir_abs = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        
        # 2. Security: Ensure it's inside the working directory
        common = os.path.commonpath([working_dir_abs, target_path])
        if common != working_dir_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
            
        # 3. Validation: Does it exist and is it a file?
        if not os.path.isfile(target_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
            
        # 4. Extension Check
        if not target_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        # 5. Build the Command
        command = ["python3", target_path]
        if args:
            command.extend(args)

        # 6. Execute with subprocess
        # text=True decodes bytes to strings automatically
        # capture_output=True grabs stdout and stderr
        result = subprocess.run(
            command,
            cwd=working_dir_abs,
            capture_output=True,
            text=True,
            timeout=30
        )

        # 7. Format the Output
        output = []
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")
        
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")
        
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")

        if not result.stdout and not result.stderr:
            output.append("No output produced")

        return "\n".join(output)

    except subprocess.TimeoutExpired:
        return "Error: The process timed out after 30 seconds."
    except Exception as e:
        return f"Error: executing Python file: {e}"