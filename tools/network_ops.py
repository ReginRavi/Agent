"""Network and web operations tools for the Gemini agent."""

import json
import subprocess
from pathlib import Path
from typing import Any
from urllib import request, parse


def _web_search(query: str, num_results: int = 5) -> str:
    """Search the web using DuckDuckGo HTML."""
    try:
        # Use DuckDuckGo HTML (no API key needed)
        url = f"https://html.duckduckgo.com/html/?q={parse.quote(query)}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        req = request.Request(url, headers=headers)
        with request.urlopen(req, timeout=10) as response:
            html = response.read().decode("utf-8")
        
        # Simple parsing - look for result links
        results = []
        lines = html.split("\n")
        for i, line in enumerate(lines):
            if 'class="result__title"' in line or 'class="result__a"' in line:
                # Try to extract the link text
                if i + 1 < len(lines):
                    text = lines[i + 1].strip()
                    # Remove HTML tags
                    text = text.replace("<b>", "").replace("</b>", "")
                    if text and len(text) > 10:
                        results.append(text[:200])  # Limit to 200 chars
                        if len(results) >= num_results:
                            break
        
        if not results:
            return f"No results found for '{query}'. (Note: Web search uses HTML scraping and may be limited.)"
        
        return f"Search results for '{query}':\n" + "\n\n".join(f"{i+1}. {r}" for i, r in enumerate(results))
    except Exception as e:
        return f"Error performing web search: {str(e)}"


def _http_request(url: str, method: str = "GET", headers: str = "", data: str = "") -> str:
    """Make an HTTP request."""
    try:
        # Parse headers if provided (JSON string)
        header_dict = {}
        if headers:
            try:
                header_dict = json.loads(headers)
            except json.JSONDecodeError:
                return "Error: Headers must be valid JSON"
        
        # Prepare request
        req_data = data.encode() if data else None
        req = request.Request(url, data=req_data, headers=header_dict, method=method)
        
        # Make request
        with request.urlopen(req, timeout=15) as response:
            status = response.status
            content = response.read().decode("utf-8")
            
            # Limit response size
            if len(content) > 5000:
                content = content[:5000] + f"\n\n... (truncated, total {len(content)} chars)"
            
            return f"HTTP {status}\n\n{content}"
    except Exception as e:
        return f"Error making HTTP request: {str(e)}"


def _execute_command(command: str, working_dir: str = ".") -> str:
    """Execute a shell command and return its output."""
    try:
        path = Path(working_dir).expanduser()
        if not path.exists():
            return f"Error: Working directory '{working_dir}' does not exist."
        
        # Security: Prevent some dangerous commands
        dangerous_patterns = ["rm -rf /", "format", "mkfs", "> /dev/"]
        if any(pattern in command.lower() for pattern in dangerous_patterns):
            return "Error: This command appears to be dangerous and is blocked."
        
        result = subprocess.run(
            command,
            shell=True,
            cwd=str(path),
            capture_output=True,
            text=True,
            timeout=30,  # 30 second timeout
        )
        
        output = []
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")
        if result.returncode != 0:
            output.append(f"Exit code: {result.returncode}")
        
        return "\n".join(output) if output else "(no output)"
    except subprocess.TimeoutExpired:
        return "Error: Command timed out after 30 seconds."
    except Exception as e:
        return f"Error executing command: {str(e)}"


def _get_current_directory() -> str:
    """Get the current working directory."""
    try:
        return str(Path.cwd())
    except Exception as e:
        return f"Error getting current directory: {str(e)}"


NETWORK_OPS_TOOLS: dict[str, dict[str, Any]] = {
    "web_search": {
        "definition": {
            "name": "web_search",
            "description": "Searches the web using DuckDuckGo and returns search results.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query.",
                    },
                    "num_results": {
                        "type": "integer",
                        "description": "Number of results to return (default 5).",
                    },
                },
                "required": ["query"],
            },
        },
        "function": _web_search,
    },
    "http_request": {
        "definition": {
            "name": "http_request",
            "description": "Make an HTTP request to a URL.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "URL to request.",
                    },
                    "method": {
                        "type": "string",
                        "description": "HTTP method (GET, POST, etc.). Default: GET.",
                    },
                    "headers": {
                        "type": "string",
                        "description": "Optional headers as JSON string.",
                    },
                    "data": {
                        "type": "string",
                        "description": "Optional request body data.",
                    },
                },
                "required": ["url"],
            },
        },
        "function": _http_request,
    },
    "execute_command": {
        "definition": {
            "name": "execute_command",
            "description": "Executes a shell command and returns its output. Has a 30-second timeout.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The shell command to execute.",
                    },
                    "working_dir": {
                        "type": "string",
                        "description": "Working directory for the command. Defaults to current directory.",
                    },
                },
                "required": ["command"],
            },
        },
        "function": _execute_command,
    },
    "get_current_directory": {
        "definition": {
            "name": "get_current_directory",
            "description": "Gets the current working directory path.",
            "parameters": {
                "type": "object",
                "properties": {},
            },
        },
        "function": _get_current_directory,
    },
}
