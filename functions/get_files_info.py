import os

def get_files_info(working_directory, directory="."):
    try:
        # 1. Get the absolute path of the permitted working directory
        working_dir_abs = os.path.abspath(working_directory)
        
        # 2. Construct and normalize the target directory path
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        
        # 3. Security Check: Is the target actually inside the working directory?
        # We find the common path between the two.
        common = os.path.commonpath([working_dir_abs, target_dir])
        if common != working_dir_abs:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        # 4. Validation: Does the directory actually exist?
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
            
        # 5. List files and build the string
        items = os.listdir(target_dir)
        output_lines = []
        
        for item in items:
            item_path = os.path.join(target_dir, item)
            size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)
            output_lines.append(f"- {item}: file_size={size} bytes, is_dir={is_dir}")
            
        # Join all lines with a newline character
        return "\n".join(output_lines)

    except Exception as e:
        return f"Error: {str(e)}"