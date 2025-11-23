"""Data processing tools for the Gemini agent."""

import csv
import json
from io import StringIO
from pathlib import Path
from typing import Any


def _read_json(file_path: str) -> str:
    """Parse and read a JSON file."""
    try:
        path = Path(file_path).expanduser()
        if not path.exists():
            return f"Error: File '{file_path}' does not exist."
        if not path.is_file():
            return f"Error: '{file_path}' is not a file."
        
        with path.open('r') as f:
            data = json.load(f)
        
        # Return formatted JSON
        return json.dumps(data, indent=2)
    except json.JSONDecodeError as e:
        return f"Error: Invalid JSON - {str(e)}"
    except Exception as e:
        return f"Error reading JSON: {str(e)}"


def _write_json(file_path: str, data: str, pretty: bool = True) -> str:
    """Write data to a JSON file."""
    try:
        path = Path(file_path).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # Parse the data to validate it's JSON
        try:
            parsed_data = json.loads(data)
        except json.JSONDecodeError:
            return "Error: Provided data is not valid JSON"
        
        # Write with or without formatting
        with path.open('w') as f:
            if pretty:
                json.dump(parsed_data, f, indent=2)
            else:
                json.dump(parsed_data, f)
        
        return f"Successfully wrote JSON to '{file_path}'"
    except Exception as e:
        return f"Error writing JSON: {str(e)}"


def _query_json(file_path: str, json_path: str) -> str:
    """Query JSON file using simple dot notation (e.g., 'user.name')."""
    try:
        path = Path(file_path).expanduser()
        if not path.exists():
            return f"Error: File '{file_path}' does not exist."
        
        with path.open('r') as f:
            data = json.load(f)
        
        # Navigate the JSON structure using dot notation
        keys = json_path.split('.')
        result = data
        
        for key in keys:
            if isinstance(result, dict) and key in result:
                result = result[key]
            elif isinstance(result, list) and key.isdigit():
                idx = int(key)
                if 0 <= idx < len(result):
                    result = result[idx]
                else:
                    return f"Error: Index {idx} out of range"
            else:
                return f"Error: Key '{key}' not found in path '{json_path}'"
        
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error querying JSON: {str(e)}"


def _read_csv(file_path: str, delimiter: str = ",") -> str:
    """Read a CSV file and return formatted table."""
    try:
        path = Path(file_path).expanduser()
        if not path.exists():
            return f"Error: File '{file_path}' does not exist."
        
        with path.open('r') as f:
            reader = csv.reader(f, delimiter=delimiter)
            rows = list(reader)
        
        if not rows:
            return "CSV file is empty"
        
        # Format as table
        result = [f"Found {len(rows)} rows, {len(rows[0]) if rows else 0} columns\n"]
        
        # Show first 20 rows
        max_rows = min(20, len(rows))
        for i, row in enumerate(rows[:max_rows]):
            result.append(f"Row {i + 1}: {', '.join(row)}")
        
        if len(rows) > max_rows:
            result.append(f"\n... and {len(rows) - max_rows} more rows")
        
        return "\n".join(result)
    except Exception as e:
        return f"Error reading CSV: {str(e)}"


def _write_csv(file_path: str, data: str, delimiter: str = ",") -> str:
    """Write CSV data to file. Data should be rows separated by newlines."""
    try:
        path = Path(file_path).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # Parse the data (assumes each line is a row, values separated by delimiter)
        rows = [line.strip().split(delimiter) for line in data.strip().split('\n')]
        
        with path.open('w', newline='') as f:
            writer = csv.writer(f, delimiter=delimiter)
            writer.writerows(rows)
        
        return f"Successfully wrote {len(rows)} rows to '{file_path}'"
    except Exception as e:
        return f"Error writing CSV: {str(e)}"


def _read_yaml(file_path: str) -> str:
    """Parse and read a YAML file."""
    try:
        path = Path(file_path).expanduser()
        if not path.exists():
            return f"Error: File '{file_path}' does not exist."
        
        try:
            import yaml
        except ImportError:
            return "Error: PyYAML not installed. Install with: pip install pyyaml"
        
        with path.open('r') as f:
            data = yaml.safe_load(f)
        
        # Return as formatted JSON (easier to read than YAML dump)
        return json.dumps(data, indent=2)
    except Exception as e:
        return f"Error reading YAML: {str(e)}"


DATA_PROCESSING_TOOLS: dict[str, dict[str, Any]] = {
    "read_json": {
        "definition": {
            "name": "read_json",
            "description": "Read and parse a JSON file, returning formatted content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the JSON file.",
                    }
                },
                "required": ["file_path"],
            },
        },
        "function": _read_json,
    },
    "write_json": {
        "definition": {
            "name": "write_json",
            "description": "Write JSON data to a file with optional pretty formatting.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to write the JSON file.",
                    },
                    "data": {
                        "type": "string",
                        "description": "JSON data as a string.",
                    },
                    "pretty": {
                        "type": "boolean",
                        "description": "Format with indentation (default: true).",
                    },
                },
                "required": ["file_path", "data"],
            },
        },
        "function": _write_json,
    },
    "query_json": {
        "definition": {
            "name": "query_json",
            "description": "Query a JSON file using dot notation (e.g., 'user.name' or 'items.0.id').",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the JSON file.",
                    },
                    "json_path": {
                        "type": "string",
                        "description": "Dot notation path to query (e.g., 'config.database.host').",
                    },
                },
                "required": ["file_path", "json_path"],
            },
        },
        "function": _query_json,
    },
    "read_csv": {
        "definition": {
            "name": "read_csv",
            "description": "Read a CSV file and return formatted table.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the CSV file.",
                    },
                    "delimiter": {
                        "type": "string",
                        "description": "Field delimiter (default: comma).",
                    },
                },
                "required": ["file_path"],
            },
        },
        "function": _read_csv,
    },
    "write_csv": {
        "definition": {
            "name": "write_csv",
            "description": "Write CSV data to file. Provide data as newline-separated rows.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to write the CSV file.",
                    },
                    "data": {
                        "type": "string",
                        "description": "CSV data (rows separated by newlines).",
                    },
                    "delimiter": {
                        "type": "string",
                        "description": "Field delimiter (default: comma).",
                    },
                },
                "required": ["file_path", "data"],
            },
        },
        "function": _write_csv,
    },
    "read_yaml": {
        "definition": {
            "name": "read_yaml",
            "description": "Read and parse a YAML file (requires pyyaml).",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the YAML file.",
                    }
                },
                "required": ["file_path"],
            },
        },
        "function": _read_yaml,
    },
}
