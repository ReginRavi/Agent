"""Environment and system tools for the Gemini agent."""

import platform
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


def _list_dir(directory_path: str) -> str:
    """Return directory entries sorted for deterministic tool outputs."""
    try:
        path = Path(directory_path).expanduser()
        if not path.exists():
            return f"Error: Directory '{directory_path}' does not exist."
        if not path.is_dir():
            return f"Error: '{directory_path}' is not a directory."
        
        entries = sorted(entry.name for entry in path.iterdir())
        return "\n".join(entries) if entries else "(empty directory)"
    except Exception as e:
        return f"Error listing directory: {str(e)}"


def _create_directory(directory_path: str) -> str:
    """Create a new directory."""
    try:
        path = Path(directory_path).expanduser()
        if path.exists():
            return f"Error: '{directory_path}' already exists."
        
        path.mkdir(parents=True, exist_ok=False)
        return f"Successfully created directory '{directory_path}'."
    except Exception as e:
        return f"Error creating directory: {str(e)}"


def _search_in_files(directory_path: str, pattern: str) -> str:
    """Search for a text pattern in files within a directory."""
    try:
        path = Path(directory_path).expanduser()
        if not path.exists():
            return f"Error: Directory '{directory_path}' does not exist."
        if not path.is_dir():
            return f"Error: '{directory_path}' is not a directory."
        
        results = []
        for file_path in path.rglob("*"):
            if file_path.is_file():
                try:
                    # Skip binary files and large files
                    if file_path.stat().st_size > 1024 * 1024:  # 1MB limit for search
                        continue
                    
                    content = file_path.read_text()
                    if pattern in content:
                        # Count occurrences
                        count = content.count(pattern)
                        results.append(f"{file_path.relative_to(path)}: {count} match(es)")
                except (UnicodeDecodeError, PermissionError):
                    # Skip binary files or files we can't read
                    continue
        
        if not results:
            return f"No matches found for '{pattern}' in '{directory_path}'."
        
        return "\n".join(results)
    except Exception as e:
        return f"Error searching files: {str(e)}"


def _get_file_info(file_path: str) -> str:
    """Get information about a file or directory."""
    try:
        path = Path(file_path).expanduser()
        if not path.exists():
            return f"Error: '{file_path}' does not exist."
        
        stat = path.stat()
        info = [
            f"Path: {file_path}",
            f"Type: {'Directory' if path.is_dir() else 'File'}",
            f"Size: {stat.st_size} bytes ({stat.st_size / 1024:.2f} KB)",
            f"Modified: {datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')}",
            f"Permissions: {oct(stat.st_mode)[-3:]}",
        ]
        
        if path.is_dir():
            try:
                num_items = len(list(path.iterdir()))
                info.append(f"Items: {num_items}")
            except PermissionError:
                info.append("Items: (permission denied)")
        
        return "\n".join(info)
    except Exception as e:
        return f"Error getting file info: {str(e)}"


def _get_environment_info() -> str:
    """Get Python and system environment information."""
    try:
        info = [
            f"Python version: {sys.version.split()[0]}",
            f"Python executable: {sys.executable}",
            f"Platform: {platform.platform()}",
            f"System: {platform.system()} {platform.release()}",
            f"Architecture: {platform.machine()}",
            f"Working directory: {Path.cwd()}",
        ]
        
        # Try to get pip list
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "list", "--format=freeze"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            if result.returncode == 0:
                packages = result.stdout.strip().split("\n")
                info.append(f"Installed packages: {len(packages)}")
                info.append("\nKey packages:")
                for pkg in packages[:10]:
                    info.append(f"  {pkg}")
                if len(packages) > 10:
                    info.append(f"  ... and {len(packages) - 10} more")
        except:
            pass
        
        return "\n".join(info)
    except Exception as e:
        return f"Error getting environment info: {str(e)}"


def _install_package(package_name: str, package_manager: str = "pip") -> str:
    """Install a Python package."""
    try:
        if package_manager != "pip":
            return "Error: Only 'pip' package manager is currently supported"
        
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", package_name],
            capture_output=True,
            text=True,
            timeout=120,
        )
        
        if result.returncode != 0:
            return f"Error installing package:\n{result.stderr}"
        
        return f"Successfully installed '{package_name}':\n{result.stdout[-500:]}"
    except subprocess.TimeoutExpired:
        return "Error: Installation timed out after 2 minutes"
    except Exception as e:
        return f"Error installing package: {str(e)}"


ENVIRONMENT_TOOLS: dict[str, dict[str, Any]] = {
    "list_dir": {
        "definition": {
            "name": "list_dir",
            "description": "Lists the contents of a directory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory_path": {
                        "type": "string",
                        "description": "Path to the directory to list.",
                    }
                },
                "required": ["directory_path"],
            },
        },
        "function": _list_dir,
    },
    "create_directory": {
        "definition": {
            "name": "create_directory",
            "description": "Creates a new directory. Creates parent directories if needed.",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory_path": {
                        "type": "string",
                        "description": "Path to the directory to create.",
                    }
                },
                "required": ["directory_path"],
            },
        },
        "function": _create_directory,
    },
    "search_in_files": {
        "definition": {
            "name": "search_in_files",
            "description": "Searches for a text pattern in all files within a directory (recursively).",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory_path": {
                        "type": "string",
                        "description": "Path to the directory to search in.",
                    },
                    "pattern": {
                        "type": "string",
                        "description": "Text pattern to search for.",
                    },
                },
                "required": ["directory_path", "pattern"],
            },
        },
        "function": _search_in_files,
    },
    "get_file_info": {
        "definition": {
            "name": "get_file_info",
            "description": "Gets information about a file or directory (size, modified time, permissions).",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the file or directory.",
                    }
                },
                "required": ["file_path"],
            },
        },
        "function": _get_file_info,
    },
    "get_environment_info": {
        "definition": {
            "name": "get_environment_info",
            "description": "Get Python version, system info, and installed packages.",
            "parameters": {
                "type": "object",
                "properties": {},
            },
        },
        "function": _get_environment_info,
    },
    "install_package": {
        "definition": {
            "name": "install_package",
            "description": "Install a Python package using pip.",
            "parameters": {
                "type": "object",
                "properties": {
                    "package_name": {
                        "type": "string",
                        "description": "Name of the package to install.",
                    },
                    "package_manager": {
                        "type": "string",
                        "description": "Package manager to use (default: pip).",
                    },
                },
                "required": ["package_name"],
            },
        },
        "function": _install_package,
    },
}
