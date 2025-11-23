"""Archive and compression tools for the Gemini agent."""

import zipfile
from pathlib import Path
from typing import Any


def _create_zip(source_path: str, zip_path: str) -> str:
    """Create a zip archive from a file or directory."""
    try:
        source = Path(source_path).expanduser()
        zip_file = Path(zip_path).expanduser()
        
        if not source.exists():
            return f"Error: Source '{source_path}' does not exist."
        
        # Create parent directories for zip file
        zip_file.parent.mkdir(parents=True, exist_ok=True)
        
        with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            if source.is_file():
                # Single file
                zf.write(source, source.name)
                file_count = 1
            else:
                # Directory - recursively add all files
                file_count = 0
                for file_path in source.rglob('*'):
                    if file_path.is_file():
                        zf.write(file_path, file_path.relative_to(source.parent))
                        file_count += 1
        
        zip_size = zip_file.stat().st_size
        return f"Successfully created '{zip_path}' with {file_count} file(s), size: {zip_size / 1024:.2f} KB"
    except Exception as e:
        return f"Error creating zip: {str(e)}"


def _extract_zip(zip_path: str, dest_path: str = ".") -> str:
    """Extract a zip archive to a destination directory."""
    try:
        zip_file = Path(zip_path).expanduser()
        dest = Path(dest_path).expanduser()
        
        if not zip_file.exists():
            return f"Error: Zip file '{zip_path}' does not exist."
        if not zip_file.is_file():
            return f"Error: '{zip_path}' is not a file."
        
        # Create destination directory
        dest.mkdir(parents=True, exist_ok=True)
        
        with zipfile.ZipFile(zip_file, 'r') as zf:
            # Get file count
            file_count = len(zf.namelist())
            
            # Extract all
            zf.extractall(dest)
        
        return f"Successfully extracted {file_count} file(s) to '{dest_path}'"
    except zipfile.BadZipFile:
        return f"Error: '{zip_path}' is not a valid zip file."
    except Exception as e:
        return f"Error extracting zip: {str(e)}"


def _list_archive(archive_path: str) -> str:
    """List contents of a zip archive."""
    try:
        archive = Path(archive_path).expanduser()
        
        if not archive.exists():
            return f"Error: Archive '{archive_path}' does not exist."
        
        with zipfile.ZipFile(archive, 'r') as zf:
            info_list = zf.infolist()
            
            if not info_list:
                return "Archive is empty"
            
            result = [f"Archive contents ({len(info_list)} items):\n"]
            
            # Show details for each file
            max_items = min(50, len(info_list))
            for info in info_list[:max_items]:
                compressed_kb = info.compress_size / 1024
                uncompressed_kb = info.file_size / 1024
                ratio = (1 - info.compress_size / info.file_size) * 100 if info.file_size > 0 else 0
                
                result.append(
                    f"  {info.filename} - "
                    f"{uncompressed_kb:.2f} KB "
                    f"(compressed: {compressed_kb:.2f} KB, "
                    f"ratio: {ratio:.1f}%)"
                )
            
            if len(info_list) > max_items:
                result.append(f"\n... and {len(info_list) - max_items} more items")
            
            return "\n".join(result)
    except zipfile.BadZipFile:
        return f"Error: '{archive_path}' is not a valid zip file."
    except Exception as e:
        return f"Error listing archive: {str(e)}"


ARCHIVE_OPS_TOOLS: dict[str, dict[str, Any]] = {
    "create_zip": {
        "definition": {
            "name": "create_zip",
            "description": "Create a zip archive from a file or directory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "source_path": {
                        "type": "string",
                        "description": "Path to file or directory to compress.",
                    },
                    "zip_path": {
                        "type": "string",
                        "description": "Path for the output zip file.",
                    },
                },
                "required": ["source_path", "zip_path"],
            },
        },
        "function": _create_zip,
    },
    "extract_zip": {
        "definition": {
            "name": "extract_zip",
            "description": "Extract a zip archive to a destination directory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "zip_path": {
                        "type": "string",
                        "description": "Path to the zip file to extract.",
                    },
                    "dest_path": {
                        "type": "string",
                        "description": "Destination directory (default: current directory).",
                    },
                },
                "required": ["zip_path"],
            },
        },
        "function": _extract_zip,
    },
    "list_archive": {
        "definition": {
            "name": "list_archive",
            "description": "List contents of a zip archive with sizes and compression ratios.",
            "parameters": {
                "type": "object",
                "properties": {
                    "archive_path": {
                        "type": "string",
                        "description": "Path to the zip archive.",
                    }
                },
                "required": ["archive_path"],
            },
        },
        "function": _list_archive,
    },
}
