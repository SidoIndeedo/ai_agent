import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    try:
        # 1. Get the absolute path of the permitted working directory
        working_dir_abs = os.path.abspath(working_directory)
        
        # 2. Construct the full path to the target file
        target_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        
        # 3. Security Check: Is it inside the working directory?
        common = os.path.commonpath([working_dir_abs, target_path])
        if common != working_dir_abs:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        # 4. Validation: Check if it's a file
        if not os.path.isfile(target_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        # 5. Read and Truncate
        with open(target_path, 'r', encoding='utf-8') as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                # Ensure this matches the exact format in your assignment
                content += f'\n[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return content
            
    except Exception as e:
        return f"Error: {str(e)}"