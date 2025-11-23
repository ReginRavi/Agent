"""File operations tools for the Gemini agent."""

from pathlib import Path
from typing import Any


def _read_file(file_path: str) -> str:
    """Read plain text from ``file_path``."""
    try:
        path = Path(file_path).expanduser()
        if not path.exists():
            return f"Error: File '{file_path}' does not exist."
        if not path.is_file():
            return f"Error: '{file_path}' is not a file."
        
        # Safety check: limit file size to 10MB
        file_size = path.stat().st_size
        if file_size > 10 * 1024 * 1024:
            return f"Error: File too large ({file_size / 1024 / 1024:.2f}MB). Maximum size is 10MB."
        
        return path.read_text()
    except Exception as e:
        return f"Error reading file: {str(e)}"


def _write_file(file_path: str, contents: str) -> str:
    """Write ``contents`` to ``file_path`` and return success."""
    try:
        path = Path(file_path).expanduser()
        # Create parent directories if they don't exist
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(contents)
        return f"Successfully wrote {len(contents)} characters to '{file_path}'."
    except Exception as e:
        return f"Error writing file: {str(e)}"


def _delete_file(file_path: str) -> str:
    """Delete a file."""
    try:
        path = Path(file_path).expanduser()
        if not path.exists():
            return f"Error: File '{file_path}' does not exist."
        if not path.is_file():
            return f"Error: '{file_path}' is not a file."
        
        path.unlink()
        return f"Successfully deleted '{file_path}'."
    except Exception as e:
        return f"Error deleting file: {str(e)}"


def _append_to_file(file_path: str, contents: str) -> str:
    """Append content to a file without overwriting."""
    try:
        path = Path(file_path).expanduser()
        
        # Create file if it doesn't exist
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(contents)
            return f"Created new file '{file_path}' with {len(contents)} characters."
        
        # Append to existing file
        with path.open("a") as f:
            f.write(contents)
        
        return f"Appended {len(contents)} characters to '{file_path}'"
    except Exception as e:
        return f"Error appending to file: {str(e)}"


def _find_replace_in_file(file_path: str, find: str, replace: str) -> str:
    """Find and replace text in a file."""
    try:
        path = Path(file_path).expanduser()
        if not path.exists():
            return f"Error: File '{file_path}' does not exist."
        if not path.is_file():
            return f"Error: '{file_path}' is not a file."
        
        content = path.read_text()
        
        if find not in content:
            return f"No occurrences of '{find}' found in '{file_path}'"
        
        count = content.count(find)
        new_content = content.replace(find, replace)
        
        path.write_text(new_content)
        
        return f"Replaced {count} occurrence(s) of '{find}' with '{replace}' in '{file_path}'"
    except Exception as e:
        return f"Error with find/replace: {str(e)}"


FILE_OPS_TOOLS: dict[str, dict[str, Any]] = {
    "read_file": {
        "definition": {
            "name": "read_file",
            "description": "Reads a file and returns its contents. Maximum file size is 10MB.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the file to read.",
                    }
                },
                "required": ["file_path"],
            },
        },
        "function": _read_file,
    },
    "write_file": {
        "definition": {
            "name": "write_file",
            "description": "Writes a file with the given contents. Creates parent directories if needed.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the file to write.",
                    },
                    "contents": {
                        "type": "string",
                        "description": "Contents to write to the file.",
                    },
                },
                "required": ["file_path", "contents"],
            },
        },
        "function": _write_file,
    },
    "delete_file": {
        "definition": {
            "name": "delete_file",
            "description": "Deletes a file from the filesystem.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the file to delete.",
                    }
                },
                "required": ["file_path"],
            },
        },
        "function": _delete_file,
    },
    "append_to_file": {
        "definition": {
            "name": "append_to_file",
            "description": "Append content to a file without overwriting existing content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the file.",
                    },
                    "contents": {
                        "type": "string",
                        "description": "Content to append.",
                    },
                },
                "required": ["file_path", "contents"],
            },
        },
        "function": _append_to_file,
    },
    "find_replace_in_file": {
        "definition": {
            "name": "find_replace_in_file",
            "description": "Find and replace text in a file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the file.",
                    },
                    "find": {
                        "type": "string",
                        "description": "Text to find.",
                    },
                    "replace": {
                        "type": "string",
                        "description": "Text to replace with.",
                    },
                },
                "required": ["file_path", "find", "replace"],
            },
        },
        "function": _find_replace_in_file,
    },
}
