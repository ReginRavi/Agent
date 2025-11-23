"""Git operations tools for the Gemini agent."""

import subprocess
from typing import Any


def _git_status() -> str:
    """Get git repository status."""
    try:
        result = subprocess.run(
            ["git", "status", "--short"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        
        if result.returncode != 0:
            return f"Error: Not a git repository or git not available.\n{result.stderr}"
        
        if not result.stdout.strip():
            return "Working tree clean (no changes)"
        
        return f"Git status:\n{result.stdout}"
    except Exception as e:
        return f"Error getting git status: {str(e)}"


def _git_diff(file_path: str = "") -> str:
    """Show git diff for a file or all files."""
    try:
        cmd = ["git", "diff"]
        if file_path:
            cmd.append(file_path)
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=15,
        )
        
        if result.returncode != 0:
            return f"Error: {result.stderr}"
        
        if not result.stdout.strip():
            return "No changes to show"
        
        # Limit output to prevent overwhelming
        lines = result.stdout.split("\n")
        if len(lines) > 200:
            return "\n".join(lines[:200]) + f"\n\n... (showing first 200 lines of {len(lines)} total)"
        
        return result.stdout
    except Exception as e:
        return f"Error getting git diff: {str(e)}"


def _git_log(num_commits: int = 10) -> str:
    """Show git commit history."""
    try:
        result = subprocess.run(
            ["git", "log", f"-{num_commits}", "--oneline", "--decorate"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        
        if result.returncode != 0:
            return f"Error: {result.stderr}"
        
        if not result.stdout.strip():
            return "No commits found"
        
        return f"Last {num_commits} commits:\n{result.stdout}"
    except Exception as e:
        return f"Error getting git log: {str(e)}"


def _git_add(file_path: str) -> str:
    """Stage a file for commit."""
    try:
        result = subprocess.run(
            ["git", "add", file_path],
            capture_output=True,
            text=True,
            timeout=10,
        )
        
        if result.returncode != 0:
            return f"Error: {result.stderr}"
        
        return f"Successfully staged '{file_path}'"
    except Exception as e:
        return f"Error staging file: {str(e)}"


def _git_commit(message: str) -> str:
    """Create a git commit."""
    try:
        if not message.strip():
            return "Error: Commit message cannot be empty"
        
        result = subprocess.run(
            ["git", "commit", "-m", message],
            capture_output=True,
            text=True,
            timeout=15,
        )
        
        if result.returncode != 0:
            return f"Error: {result.stderr}"
        
        return f"Successfully created commit:\n{result.stdout}"
    except Exception as e:
        return f"Error creating commit: {str(e)}"


def _git_branch(operation: str = "list", branch_name: str = "") -> str:
    """Git branch operations: list, create, or switch."""
    try:
        if operation == "list":
            result = subprocess.run(
                ["git", "branch", "-a"],
                capture_output=True,
                text=True,
                timeout=10,
            )
        elif operation == "create":
            if not branch_name:
                return "Error: Branch name required for create operation"
            result = subprocess.run(
                ["git", "branch", branch_name],
                capture_output=True,
                text=True,
                timeout=10,
            )
        elif operation == "switch":
            if not branch_name:
                return "Error: Branch name required for switch operation"
            result = subprocess.run(
                ["git", "checkout", branch_name],
                capture_output=True,
                text=True,
                timeout=10,
            )
        else:
            return f"Error: Unknown operation '{operation}'. Use: list, create, or switch"
        
        if result.returncode != 0:
            return f"Error: {result.stderr}"
        
        output = result.stdout if result.stdout.strip() else result.stderr
        return output if output.strip() else f"Operation '{operation}' completed successfully"
    except Exception as e:
        return f"Error with git branch operation: {str(e)}"


def _git_pull(remote: str = "origin", branch: str = "") -> str:
    """Pull latest changes from remote repository."""
    try:
        cmd = ["git", "pull", remote]
        if branch:
            cmd.append(branch)
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60,  # Longer timeout for network operation
        )
        
        if result.returncode != 0:
            return f"Error: {result.stderr}"
        
        return f"Pull from '{remote}' successful:\n{result.stdout}"
    except subprocess.TimeoutExpired:
        return "Error: Pull operation timed out after 60 seconds"
    except Exception as e:
        return f"Error pulling from remote: {str(e)}"


def _git_push(remote: str = "origin", branch: str = "") -> str:
    """Push commits to remote repository."""
    try:
        cmd = ["git", "push", remote]
        if branch:
            cmd.append(branch)
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60,  # Longer timeout for network operation
        )
        
        if result.returncode != 0:
            return f"Error: {result.stderr}"
        
        return f"Push to '{remote}' successful:\n{result.stdout if result.stdout else result.stderr}"
    except subprocess.TimeoutExpired:
        return "Error: Push operation timed out after 60 seconds"
    except Exception as e:
        return f"Error pushing to remote: {str(e)}"


def _git_stash(operation: str = "save") -> str:
    """Stash changes: save, pop, list, or show."""
    try:
        if operation == "save":
            cmd = ["git", "stash", "save"]
        elif operation == "pop":
            cmd = ["git", "stash", "pop"]
        elif operation == "list":
            cmd = ["git", "stash", "list"]
        elif operation == "show":
            cmd = ["git", "stash", "show", "-p"]
        else:
            return f"Error: Unknown operation '{operation}'. Use: save, pop, list, or show"
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=15,
        )
        
        if result.returncode != 0 and result.stderr:
            return f"Error: {result.stderr}"
        
        output = result.stdout if result.stdout.strip() else result.stderr
        
        if not output.strip():
            if operation == "list":
                return "No stashed changes"
            elif operation == "save":
                return "No local changes to save"
            else:
                return f"Stash {operation} completed"
        
        return output
    except Exception as e:
        return f"Error with git stash: {str(e)}"


def _git_remote(operation: str = "list") -> str:
    """Git remote operations: list, add, remove."""
    try:
        if operation == "list":
            result = subprocess.run(
                ["git", "remote", "-v"],
                capture_output=True,
                text=True,
                timeout=10,
            )
        else:
            return f"Error: Unknown operation '{operation}'. Currently only 'list' is supported"
        
        if result.returncode != 0:
            return f"Error: {result.stderr}"
        
        if not result.stdout.strip():
            return "No remotes configured"
        
        return f"Remote repositories:\n{result.stdout}"
    except Exception as e:
        return f"Error with git remote: {str(e)}"


GIT_OPS_TOOLS: dict[str, dict[str, Any]] = {
    "git_status": {
        "definition": {
            "name": "git_status",
            "description": "Get the current git repository status.",
            "parameters": {
                "type": "object",
                "properties": {},
            },
        },
        "function": _git_status,
    },
    "git_diff": {
        "definition": {
            "name": "git_diff",
            "description": "Show git diff for a specific file or all files.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Optional file path to show diff for. If empty, shows diff for all files.",
                    }
                },
            },
        },
        "function": _git_diff,
    },
    "git_log": {
        "definition": {
            "name": "git_log",
            "description": "Show git commit history.",
            "parameters": {
                "type": "object",
                "properties": {
                    "num_commits": {
                        "type": "integer",
                        "description": "Number of commits to show (default 10).",
                    }
                },
            },
        },
        "function": _git_log,
    },
    "git_add": {
        "definition": {
            "name": "git_add",
            "description": "Stage a file for commit.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the file to stage.",
                    }
                },
                "required": ["file_path"],
            },
        },
        "function": _git_add,
    },
    "git_commit": {
        "definition": {
            "name": "git_commit",
            "description": "Create a git commit with the given message.",
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "Commit message.",
                    }
                },
                "required": ["message"],
            },
        },
        "function": _git_commit,
    },
    "git_branch": {
        "definition": {
            "name": "git_branch",
            "description": "Git branch operations: list, create, or switch branches.",
            "parameters": {
                "type": "object",
                "properties": {
                    "operation": {
                        "type": "string",
                        "description": "Operation to perform: 'list', 'create', or 'switch'.",
                    },
                    "branch_name": {
                        "type": "string",
                        "description": "Branch name for create/switch operations.",
                    },
                },
            },
        },
        "function": _git_branch,
    },
    "git_pull": {
        "definition": {
            "name": "git_pull",
            "description": "Pull latest changes from a remote repository.",
            "parameters": {
                "type": "object",
                "properties": {
                    "remote": {
                        "type": "string",
                        "description": "Remote name (default: origin).",
                    },
                    "branch": {
                        "type": "string",
                        "description": "Branch name (optional).",
                    },
                },
            },
        },
        "function": _git_pull,
    },
    "git_push": {
        "definition": {
            "name": "git_push",
            "description": "Push commits to a remote repository.",
            "parameters": {
                "type": "object",
                "properties": {
                    "remote": {
                        "type": "string",
                        "description": "Remote name (default: origin).",
                    },
                    "branch": {
                        "type": "string",
                        "description": "Branch name (optional).",
                    },
                },
            },
        },
        "function": _git_push,
    },
    "git_stash": {
        "definition": {
            "name": "git_stash",
            "description": "Stash operations: save, pop, list, or show stashed changes.",
            "parameters": {
                "type": "object",
                "properties": {
                    "operation": {
                        "type": "string",
                        "description": "Operation: 'save', 'pop', 'list', or 'show' (default: save).",
                    }
                },
            },
        },
        "function": _git_stash,
    },
    "git_remote": {
        "definition": {
            "name": "git_remote",
            "description": "List remote repositories with their URLs.",
            "parameters": {
                "type": "object",
                "properties": {
                    "operation": {
                        "type": "string",
                        "description": "Operation: 'list' (default).",
                    }
                },
            },
        },
        "function": _git_remote,
    },
}
