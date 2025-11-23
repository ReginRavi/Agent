"""
Tool registry for the Gemini agent.

This module aggregates all tools from the specialized modules.
"""

from .archive_ops import ARCHIVE_OPS_TOOLS
from .code_analysis import CODE_ANALYSIS_TOOLS
from .data_processing import DATA_PROCESSING_TOOLS
from .environment import ENVIRONMENT_TOOLS
from .file_ops import FILE_OPS_TOOLS
from .git_ops import GIT_OPS_TOOLS
from .network_ops import NETWORK_OPS_TOOLS
from .system_monitoring import SYSTEM_MONITORING_TOOLS
from .text_utils import TEXT_UTILS_TOOLS

# Aggregate all tools into a single registry
ALL_TOOLS = {
    **FILE_OPS_TOOLS,           # 5 tools: file operations
    **GIT_OPS_TOOLS,            # 10 tools: git operations (6 + 4 new)
    **CODE_ANALYSIS_TOOLS,      # 3 tools: code analysis
    **NETWORK_OPS_TOOLS,        # 4 tools: network operations
    **ENVIRONMENT_TOOLS,        # 6 tools: environment & system
    **DATA_PROCESSING_TOOLS,    # 6 tools: JSON, CSV, YAML
    **TEXT_UTILS_TOOLS,         # 5 tools: text manipulation
    **ARCHIVE_OPS_TOOLS,        # 3 tools: archive operations
    **SYSTEM_MONITORING_TOOLS,  # 2 tools: system monitoring
}

# Verify we have all 44 tools
assert len(ALL_TOOLS) == 44, f"Expected 44 tools, got {len(ALL_TOOLS)}"

__all__ = ["ALL_TOOLS"]
