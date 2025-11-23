"""System monitoring tools for the Gemini agent."""

import subprocess
from typing import Any


def _list_processes(filter_name: str = "") -> str:
    """List running processes, optionally filtered by name."""
    try:
        # Try using ps command (cross-platform)
        result = subprocess.run(
            ["ps", "aux"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        
        if result.returncode != 0:
            return f"Error: Failed to get process list.\n{result.stderr}"
        
        lines = result.stdout.split('\n')
        
        # Filter if requested
        if filter_name:
            header = lines[0] if lines else ""
            filtered = [line for line in lines[1:] if filter_name.lower() in line.lower()]
            
            if not filtered:
                return f"No processes found matching '{filter_name}'"
            
            result_lines = [f"Found {len(filtered)} process(es) matching '{filter_name}':\n", header]
            result_lines.extend(filtered[:50])  # Limit to 50 results
            
            if len(filtered) > 50:
                result_lines.append(f"\n... and {len(filtered) - 50} more processes")
            
            return "\n".join(result_lines)
        else:
            # Show all processes (limited to 50)
            max_lines = min(51, len(lines))  # Header + 50 processes
            result_lines = lines[:max_lines]
            
            if len(lines) > max_lines:
                result_lines.append(f"\n... and {len(lines) - max_lines} more processes")
            
            return "\n".join(result_lines)
            
    except Exception as e:
        return f"Error listing processes: {str(e)}"


def _get_system_stats() -> str:
    """Get system resource usage statistics."""
    try:
        # Try to use psutil if available
        try:
            import psutil
            
            # Get CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            
            # Get memory usage
            memory = psutil.virtual_memory()
            
            # Get disk usage
            disk = psutil.disk_usage('/')
            
            result = [
                "System Resource Usage:",
                f"\nCPU:",
                f"  Usage: {cpu_percent}%",
                f"  Cores: {cpu_count}",
                f"\nMemory:",
                f"  Total: {memory.total / (1024**3):.2f} GB",
                f"  Used: {memory.used / (1024**3):.2f} GB ({memory.percent}%)",
                f"  Available: {memory.available / (1024**3):.2f} GB",
                f"\nDisk (/):",
                f"  Total: {disk.total / (1024**3):.2f} GB",
                f"  Used: {disk.used / (1024**3):.2f} GB ({disk.percent}%)",
                f"  Free: {disk.free / (1024**3):.2f} GB",
            ]
            
            return "\n".join(result)
            
        except ImportError:
            # Fallback to system commands
            result = ["System Stats (using system commands):\n"]
            
            # Try to get load average on Unix
            try:
                uptime_result = subprocess.run(
                    ["uptime"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                if uptime_result.returncode == 0:
                    result.append(f"Uptime: {uptime_result.stdout.strip()}")
            except:
                pass
            
            # Try to get disk usage
            try:
                df_result = subprocess.run(
                    ["df", "-h", "/"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                if df_result.returncode == 0:
                    result.append(f"\nDisk Usage:\n{df_result.stdout}")
            except:
                pass
            
            if len(result) == 1:
                result.append("Note: Install 'psutil' for detailed stats: pip install psutil")
            
            return "\n".join(result)
            
    except Exception as e:
        return f"Error getting system stats: {str(e)}"


SYSTEM_MONITORING_TOOLS: dict[str, dict[str, Any]] = {
    "list_processes": {
        "definition": {
            "name": "list_processes",
            "description": "List running processes, optionally filtered by name.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filter_name": {
                        "type": "string",
                        "description": "Optional filter to show only processes matching this name.",
                    }
                },
            },
        },
        "function": _list_processes,
    },
    "get_system_stats": {
        "definition": {
            "name": "get_system_stats",
            "description": "Get CPU, memory, and disk usage statistics. Requires psutil for detailed stats.",
            "parameters": {
                "type": "object",
                "properties": {},
            },
        },
        "function": _get_system_stats,
    },
}
