"""Text utility tools for the Gemini agent."""

import base64
import re
from typing import Any


def _regex_search(text: str, pattern: str) -> str:
    """Search for regex pattern in text and return matches."""
    try:
        matches = re.findall(pattern, text)
        
        if not matches:
            return f"No matches found for pattern: {pattern}"
        
        result = [f"Found {len(matches)} match(es):\n"]
        
        # Show first 50 matches
        max_matches = min(50, len(matches))
        for i, match in enumerate(matches[:max_matches], 1):
            if isinstance(match, tuple):
                result.append(f"{i}. {', '.join(match)}")
            else:
                result.append(f"{i}. {match}")
        
        if len(matches) > max_matches:
            result.append(f"\n... and {len(matches) - max_matches} more matches")
        
        return "\n".join(result)
    except re.error as e:
        return f"Error: Invalid regex pattern - {str(e)}"
    except Exception as e:
        return f"Error in regex search: {str(e)}"


def _regex_replace(text: str, pattern: str, replacement: str) -> str:
    """Replace all occurrences of regex pattern in text."""
    try:
        result = re.sub(pattern, replacement, text)
        count = len(re.findall(pattern, text))
        
        return f"Replaced {count} occurrence(s). Result:\n\n{result}"
    except re.error as e:
        return f"Error: Invalid regex pattern - {str(e)}"
    except Exception as e:
        return f"Error in regex replace: {str(e)}"


def _format_text(text: str, operation: str) -> str:
    """Format text with various case/style operations."""
    try:
        if operation == "upper":
            result = text.upper()
        elif operation == "lower":
            result = text.lower()
        elif operation == "title":
            result = text.title()
        elif operation == "capitalize":
            result = text.capitalize()
        elif operation == "snake_case":
            # Convert to snake_case
            result = re.sub(r'(?<!^)(?=[A-Z])', '_', text).lower()
            result = re.sub(r'\s+', '_', result)
            result = re.sub(r'-+', '_', result)
        elif operation == "camelCase":
            # Convert to camelCase
            words = re.split(r'[_\s-]+', text.lower())
            result = words[0] + ''.join(word.capitalize() for word in words[1:])
        elif operation == "PascalCase":
            # Convert to PascalCase
            words = re.split(r'[_\s-]+', text.lower())
            result = ''.join(word.capitalize() for word in words)
        elif operation == "kebab-case":
            # Convert to kebab-case
            result = re.sub(r'(?<!^)(?=[A-Z])', '-', text).lower()
            result = re.sub(r'\s+', '-', result)
            result = re.sub(r'_+', '-', result)
        else:
            return f"Error: Unknown operation '{operation}'. Use: upper, lower, title, capitalize, snake_case, camelCase, PascalCase, kebab-case"
        
        return result
    except Exception as e:
        return f"Error formatting text: {str(e)}"


def _encode_base64(text: str) -> str:
    """Encode text to base64."""
    try:
        encoded = base64.b64encode(text.encode('utf-8')).decode('utf-8')
        return f"Base64 encoded:\n{encoded}"
    except Exception as e:
        return f"Error encoding base64: {str(e)}"


def _decode_base64(encoded: str) -> str:
    """Decode base64 text."""
    try:
        decoded = base64.b64decode(encoded.encode('utf-8')).decode('utf-8')
        return f"Decoded:\n{decoded}"
    except Exception as e:
        return f"Error decoding base64: {str(e)}"


TEXT_UTILS_TOOLS: dict[str, dict[str, Any]] = {
    "regex_search": {
        "definition": {
            "name": "regex_search",
            "description": "Search for regex pattern in text and return all matches.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Text to search in.",
                    },
                    "pattern": {
                        "type": "string",
                        "description": "Regex pattern to search for.",
                    },
                },
                "required": ["text", "pattern"],
            },
        },
        "function": _regex_search,
    },
    "regex_replace": {
        "definition": {
            "name": "regex_replace",
            "description": "Replace all occurrences of regex pattern in text.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Text to perform replacement on.",
                    },
                    "pattern": {
                        "type": "string",
                        "description": "Regex pattern to find.",
                    },
                    "replacement": {
                        "type": "string",
                        "description": "Replacement string.",
                    },
                },
                "required": ["text", "pattern", "replacement"],
            },
        },
        "function": _regex_replace,
    },
    "format_text": {
        "definition": {
            "name": "format_text",
            "description": "Format text with case/style operations: upper, lower, title, capitalize, snake_case, camelCase, PascalCase, kebab-case.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Text to format.",
                    },
                    "operation": {
                        "type": "string",
                        "description": "Formatting operation to apply.",
                    },
                },
                "required": ["text", "operation"],
            },
        },
        "function": _format_text,
    },
    "encode_base64": {
        "definition": {
            "name": "encode_base64",
            "description": "Encode text to base64.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Text to encode.",
                    }
                },
                "required": ["text"],
            },
        },
        "function": _encode_base64,
    },
    "decode_base64": {
        "definition": {
            "name": "decode_base64",
            "description": "Decode base64 encoded text.",
            "parameters": {
                "type": "object",
                "properties": {
                    "encoded": {
                        "type": "string",
                        "description": "Base64 encoded string.",
                    }
                },
                "required": ["encoded"],
            },
        },
        "function": _decode_base64,
    },
}
