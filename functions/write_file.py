import os
from google import genai
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Creates a new file or overwrites an existing one with specified content. Automatically creates parent directories if they don't exist.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path where the file should be written (e.g., 'notes.txt' or 'pkg/new_module.py').",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The full text content to be written into the file.",
            ),
        },
        required=["file_path", "content"],
    ),
)

def write_file(working_directory, file_path, content):
    try:
        # 1. Path Safety & Normalization
        working_dir_abs = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        
        # 2. Security: Ensure the target is inside the working directory
        common = os.path.commonpath([working_dir_abs, target_path])
        if common != working_dir_abs:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
            
        # 3. Check if the path is actually a directory (can't overwrite a folder with text)
        if os.path.isdir(target_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
            
        # 4. Create missing parent directories
        # os.path.dirname gets the folder part of the path (e.g., "pkg/subdir")
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        
        # 5. Write the file
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(content)
            
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {str(e)}"