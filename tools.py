import os
import json
from agent import ToolDefinition

def read_file(input: dict) -> str:
    path = input["path"]
    with open(path, "r") as f:
        return f.read()

ReadFileDefinition = ToolDefinition(
    name="read_file",
    description="Read the contents of a given relative file path. Use this when you want to see what's inside a file. Do not use this with directory names.",
    input_schema={
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "The relative path of a file in the working directory.",
            }
        },
        "required": ["path"],
    },
    function=read_file,
)

def list_files(input: dict) -> str:
    path = input.get("path", ".")
    if not path:
        path = "."

    # Only list immediate children, don't recurse (avoids venv explosion)
    files = []
    try:
        for entry in os.listdir(path):
            full_path = os.path.join(path, entry)
            if os.path.isdir(full_path):
                files.append(entry + "/")
            else:
                files.append(entry)
    except OSError as e:
        return json.dumps({"error": str(e)})

    return json.dumps(sorted(files))

ListFilesDefinition = ToolDefinition(
    name="list_files",
    description="List files and directories at a given path. If no path is provided, lists files in the current directory.",
    input_schema={
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Optional relative path to list files from. Defaults to current directory if not provided.",
            }
        },
        "required": [],
    },
    function=list_files,
)


def edit_file(input: dict) -> str:
    path = input.get("path", "")
    old_str = input.get("old_str", "")
    new_str = input.get("new_str", "")

    # Validate inputs
    if not path:
        raise ValueError("path is required")
    if old_str == new_str:
        raise ValueError("old_str and new_str must be different")

    # If file doesn't exist and old_str is empty, create new file
    if not os.path.exists(path):
        if old_str == "":
            return create_new_file(path, new_str)
        raise FileNotFoundError(f"File not found: {path}")

    # Read existing content
    with open(path, "r") as f:
        content = f.read()

    # Check that old_str exists in file
    if old_str and old_str not in content:
        raise ValueError("old_str not found in file")

    # Replace old_str with new_str
    new_content = content.replace(old_str, new_str)

    # Write back
    with open(path, "w") as f:
        f.write(new_content)

    return "OK"


def create_new_file(file_path: str, content: str) -> str:
    """Helper to create a new file, including parent directories if needed."""
    dir_path = os.path.dirname(file_path)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)

    with open(file_path, "w") as f:
        f.write(content)

    return f"Successfully created file {file_path}"


EditFileDefinition = ToolDefinition(
    name="edit_file",
    description="""Make edits to a text file.

Replaces 'old_str' with 'new_str' in the given file. 'old_str' and 'new_str' MUST be different from each other.

If the file specified with path doesn't exist, it will be created.""",
    input_schema={
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "The path to the file",
            },
            "old_str": {
                "type": "string",
                "description": "Text to search for - must match exactly and must only have one match exactly",
            },
            "new_str": {
                "type": "string",
                "description": "Text to replace old_str with",
            },
        },
        "required": ["path", "old_str", "new_str"],
    },
    function=edit_file,
)