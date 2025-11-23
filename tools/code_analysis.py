"""Code analysis tools for the Gemini agent."""

import re
from pathlib import Path
from typing import Any


def _analyze_code(file_path: str) -> str:
    """Analyze a code file: syntax check, line count, and structure."""
    try:
        path = Path(file_path).expanduser()
        if not path.exists():
            return f"Error: File '{file_path}' does not exist."
        if not path.is_file():
            return f"Error: '{file_path}' is not a file."
        
        content = path.read_text()
        lines = content.split("\n")
        
        info = [
            f"File: {file_path}",
            f"Total lines: {len(lines)}",
            f"Non-empty lines: {sum(1 for line in lines if line.strip())}",
            f"Size: {len(content)} bytes",
        ]
        
        # Python-specific analysis
        if file_path.endswith(".py"):
            # Syntax check
            try:
                compile(content, file_path, "exec")
                info.append("Python syntax: ✓ Valid")
            except SyntaxError as e:
                info.append(f"Python syntax: ✗ Error on line {e.lineno}: {e.msg}")
            
            # Count imports, functions, classes
            imports = len([l for l in lines if l.strip().startswith(("import ", "from "))])
            functions = len([l for l in lines if l.strip().startswith("def ")])
            classes = len([l for l in lines if l.strip().startswith("class ")])
            
            info.append(f"Imports: {imports}")
            info.append(f"Functions: {functions}")
            info.append(f"Classes: {classes}")
        
        return "\n".join(info)
    except Exception as e:
        return f"Error analyzing code: {str(e)}"


def _find_todos(directory_path: str) -> str:
    """Find TODO, FIXME, HACK comments in code files."""
    try:
        path = Path(directory_path).expanduser()
        if not path.exists():
            return f"Error: Directory '{directory_path}' does not exist."
        if not path.is_dir():
            return f"Error: '{directory_path}' is not a directory."
        
        patterns = [r"TODO", r"FIXME", r"HACK", r"XXX", r"NOTE"]
        results = []
        
        for file_path in path.rglob("*"):
            if file_path.is_file() and file_path.suffix in [".py", ".js", ".java", ".cpp", ".c", ".go", ".rs"]:
                try:
                    content = file_path.read_text()
                    for i, line in enumerate(content.split("\n"), 1):
                        for pattern in patterns:
                            if re.search(pattern, line, re.IGNORECASE):
                                results.append(f"{file_path.relative_to(path)}:{i}: {line.strip()}")
                                break
                except (UnicodeDecodeError, PermissionError):
                    continue
        
        if not results:
            return f"No TODO/FIXME comments found in '{directory_path}'"
        
        # Limit to 50 results
        if len(results) > 50:
            return "\n".join(results[:50]) + f"\n\n... (showing first 50 of {len(results)} total)"
        
        return "\n".join(results)
    except Exception as e:
        return f"Error finding TODOs: {str(e)}"


def _count_code_lines(directory_path: str, extensions: str = ".py") -> str:
    """Count lines of code by file type."""
    try:
        path = Path(directory_path).expanduser()
        if not path.exists():
            return f"Error: Directory '{directory_path}' does not exist."
        if not path.is_dir():
            return f"Error: '{directory_path}' is not a directory."
        
        # Parse extensions
        ext_list = [e.strip() if e.startswith(".") else f".{e.strip()}" 
                   for e in extensions.split(",")]
        
        stats = {"total_files": 0, "total_lines": 0, "code_lines": 0, "blank_lines": 0, "comment_lines": 0}
        
        for file_path in path.rglob("*"):
            if file_path.is_file() and file_path.suffix in ext_list:
                try:
                    content = file_path.read_text()
                    lines = content.split("\n")
                    stats["total_files"] += 1
                    stats["total_lines"] += len(lines)
                    
                    for line in lines:
                        stripped = line.strip()
                        if not stripped:
                            stats["blank_lines"] += 1
                        elif stripped.startswith("#") or stripped.startswith("//"):
                            stats["comment_lines"] += 1
                        else:
                            stats["code_lines"] += 1
                except (UnicodeDecodeError, PermissionError):
                    continue
        
        if stats["total_files"] == 0:
            return f"No files found with extensions: {extensions}"
        
        return f"""Code statistics for {directory_path} ({extensions}):
Files: {stats['total_files']}
Total lines: {stats['total_lines']}
Code lines: {stats['code_lines']}
Blank lines: {stats['blank_lines']}
Comment lines: {stats['comment_lines']}"""
    except Exception as e:
        return f"Error counting code lines: {str(e)}"


CODE_ANALYSIS_TOOLS: dict[str, dict[str, Any]] = {
    "analyze_code": {
        "definition": {
            "name": "analyze_code",
            "description": "Analyze a code file: syntax check, line count, structure (functions, classes).",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the code file to analyze.",
                    }
                },
                "required": ["file_path"],
            },
        },
        "function": _analyze_code,
    },
    "find_todos": {
        "definition": {
            "name": "find_todos",
            "description": "Find TODO, FIXME, HACK, and NOTE comments in code files.",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory_path": {
                        "type": "string",
                        "description": "Directory to search in.",
                    }
                },
                "required": ["directory_path"],
            },
        },
        "function": _find_todos,
    },
    "count_code_lines": {
        "definition": {
            "name": "count_code_lines",
            "description": "Count lines of code by file type (code, blank, comments).",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory_path": {
                        "type": "string",
                        "description": "Directory to analyze.",
                    },
                    "extensions": {
                        "type": "string",
                        "description": "Comma-separated file extensions (e.g., '.py,.js').",
                    },
                },
                "required": ["directory_path"],
            },
        },
        "function": _count_code_lines,
    },
}
