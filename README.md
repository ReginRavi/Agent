# Enhanced Gemini AI Agent - Developer Edition v3.0

A powerful, modular AI coding assistant built with Google's Gemini 2.0 Flash API, equipped with 44 specialized tools for comprehensive development workflows.

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Gemini](https://img.shields.io/badge/Gemini-2.0%20Flash-orange.svg)](https://ai.google.dev/)

## 🎯 Purpose

This project transforms Google's Gemini AI into a **comprehensive development assistant** that can understand natural language instructions and execute complex development tasks through an extensive toolkit. It bridges the gap between conversational AI and practical development work.

## 🚀 Problem Statement

### Challenges in Modern Development

1. **Context Switching Overhead**: Developers constantly switch between:
   - Code editors
   - Terminal commands
   - Git operations
   - File management
   - Documentation lookup
   - System monitoring

2. **Repetitive Tasks**: Common operations like:
   - File manipulation (read, write, search)
   - Git workflows (status, commit, push)
   - Code analysis (syntax checking, TODOs)
   - Data processing (JSON, CSV parsing)
   
3. **Tool Fragmentation**: Different tools for different tasks:
   - Shell scripts for automation
   - Git commands for version control
   - Text editors for file editing
   - Archive utilities for compression
   - System monitors for resource checking

4. **Cognitive Load**: Remembering:
   - Command syntax and flags
   - File paths and locations
   - Git commands and workflows
   - Regex patterns for text processing

## 💡 Solution

This AI agent consolidates **44 specialized tools** into a single conversational interface where you can:

- **Speak naturally**: "Show me the git status and stage all Python files"
- **Chain operations**: "Read config.json, update the version, and commit the changes"
- **Automate workflows**: "Analyze all code, find TODOs, create a zip backup, and push to remote"

### Core Capabilities

#### 1. **File Operations** (5 tools)
- Read/write files with safety limits (10MB cap)
- Delete, append, find/replace operations
- Automatic parent directory creation

**Problem Solved**: No more manual file manipulation or complex sed/awk commands.

#### 2. **Git Workflow** (10 tools)
- Complete version control: status, diff, log, add, commit
- Branch management: create, switch, list
- Remote operations: pull, push, stash
- Remote repository management

**Problem Solved**: Full Git workflow in natural language, no need to remember commands.

#### 3. **Code Analysis** (3 tools)
- Syntax validation (Python focus)
- TODO/FIXME/HACK comment discovery
- Lines of code statistics

**Problem Solved**: Quick code quality checks without additional tools.

#### 4. **Data Processing** (6 tools)
- JSON: read, write, query with dot notation
- CSV: parse, write, format tables
- YAML: read and parse

**Problem Solved**: Work with structured data without writing custom parsers.

#### 5. **Text Manipulation** (5 tools)
- Regex search and replace
- Case conversion (camelCase, snake_case, PascalCase, kebab-case)
- Base64 encoding/decoding

**Problem Solved**: Complex text transformations without external tools.

#### 6. **Archive Operations** (3 tools)
- Create ZIP archives from files/directories
- Extract archives
- List contents with compression details

**Problem Solved**: File compression and backup without separate utilities.

#### 7. **Network Operations** (4 tools)
- Web search (DuckDuckGo integration)
- HTTP requests (GET/POST)
- Command execution with safety checks
- Current directory tracking

**Problem Solved**: API testing and web queries from the same interface.

#### 8. **System Monitoring** (2 tools)
- Process listing with filtering
- Resource usage (CPU, memory, disk)

**Problem Solved**: System monitoring without separate tools.

#### 9. **Environment Management** (6 tools)
- Directory operations (list, create, search)
- File metadata
- Python environment info
- Package installation

**Problem Solved**: Complete environment control in conversational form.

## 🏗️ Architecture

### Modular Design

```
agent1/
├── agent.py                    # Core agent (137 lines)
├── tools/                      # Modular tool library
│   ├── __init__.py            # Tool registry
│   ├── file_ops.py            # File operations (5 tools)
│   ├── git_ops.py             # Git workflow (10 tools)
│   ├── code_analysis.py       # Code quality (3 tools)
│   ├── network_ops.py         # Network & web (4 tools)
│   ├── environment.py         # System & env (6 tools)
│   ├── data_processing.py     # JSON/CSV/YAML (6 tools)
│   ├── text_utils.py          # Text manipulation (5 tools)
│   ├── archive_ops.py         # ZIP operations (3 tools)
│   └── system_monitoring.py   # Resource stats (2 tools)
└── run.sh                      # Startup script
```

**Benefits**:
- ✅ **Maintainable**: Each module ~200-250 lines
- ✅ **Extensible**: Add new tools by creating/extending modules
- ✅ **Testable**: Independent module testing
- ✅ **Clean**: Main agent file is only 137 lines

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- Google Gemini API key ([Get one here](https://ai.google.dev/))

### Setup

```bash
# Clone the repository
git clone https://github.com/ReginRavi/Agent.git
cd Agent

# Set your Gemini API key
export GEMINI_API_KEY='your-api-key-here'

# Run the agent (auto-creates venv and installs dependencies)
./run.sh
```

The `run.sh` script automatically:
1. Creates a Python virtual environment
2. Installs required packages (`google-genai`)
3. Validates your API key
4. Starts the agent

## 📚 Usage Examples

### Basic File Operations
```
You: Read the config.json file
Agent: [Shows formatted JSON content]

You: Create a new file called test.py with a hello world function
Agent: [Creates file with code]

You: Find all occurrences of 'TODO' in the codebase
Agent: [Lists all TODO comments with file locations]
```

### Git Workflow
```
You: Show me the git status
Agent: [Shows modified files]

You: Stage all Python files and commit with message "Add new features"
Agent: [Executes git add *.py && git commit -m "..."]

You: Push to origin main
Agent: [Pushes changes to remote]
```

### Data Processing
```
You: Read package.json and show me the version number
Agent: [Uses query_json with path "version"]

You: Parse users.csv and tell me how many entries there are
Agent: [Reads CSV and counts rows]
```

### Text Manipulation
```
You: Convert 'my_variable_name' to camelCase
Agent: myVariableName

You: Find all email addresses in this text using regex
Agent: [Uses regex_search with email pattern]
```

### System Operations
```
You: Show me all Python processes running
Agent: [Lists processes filtered by 'python']

You: What's my current CPU and memory usage?
Agent: [Shows system statistics]
```

## 🎨 Key Features

### 1. Natural Language Interface
No need to remember command syntax - just ask in plain English.

### 2. Chain Operations
The agent intelligently chains multiple tools to complete complex tasks.

### 3. Safety Built-in
- File size limits (10MB for reads, 1MB for searches)
- Command execution blocklist (prevents dangerous operations)
- Timeouts on all operations
- Input validation

### 4. Smart Error Handling
Every tool includes comprehensive error handling with helpful messages.

### 5. Conversational Personality
Responds like Linus Torvalds - direct, technical, and opinionated.

## 🔒 Security Features

- **Dangerous Command Blocking**: Prevents destructive commands like `rm -rf /`
- **File Size Limits**: Protects against memory exhaustion
- **Operation Timeouts**: All operations have reasonable timeouts
- **Input Validation**: Path validation and existence checks
- **Sandboxed Execution**: Commands run with 30s timeout limit

## 🔧 Configuration

### Optional Dependencies

For enhanced features:
```bash
# YAML support
pip install pyyaml

# Detailed system stats
pip install psutil
```

The agent can install these itself using its `install_package` tool!

### Environment Variables

```bash
# Required
export GEMINI_API_KEY='your-key'

# Optional (defaults shown)
export AGENT_TIMEOUT=30        # Command timeout in seconds
export AGENT_MAX_FILE_SIZE=10  # Max file size in MB
```

## 📊 Statistics

- **Total Tools**: 44
- **Code Modules**: 10 (9 tool modules + 1 core)
- **Total Lines**: ~2,200
- **Main Agent**: 137 lines (89% reduction from monolithic design)
- **Test Coverage**: Manual verification across all tools

## 🚧 Roadmap

### Potential Future Enhancements
- [ ] Database operations (SQLite, PostgreSQL)
- [ ] Docker container management
- [ ] Testing framework integration
- [ ] Code refactoring tools
- [ ] AI-powered code review
- [ ] Multi-language support (beyond Python)

## 🤝 Contributing

Contributions welcome! The modular architecture makes it easy to add new tools:

1. Create a new module in `tools/`
2. Define functions and tool dictionary
3. Import in `tools/__init__.py`
4. Update tool count assertion

## 📝 License

MIT License - feel free to use and modify!

## 🙏 Acknowledgments

- Built with [Google Gemini 2.0 Flash](https://ai.google.dev/)
- Inspired by the need for a unified development assistant
- Architecture influenced by modern software design principles

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/ReginRavi/Agent/issues)
- **Documentation**: See `walkthrough.md` in artifacts
- **Author**: Regin Ravi

## 🌟 Why This Matters

In an age where developers use dozens of tools daily, this agent demonstrates that **conversational AI can unify common development workflows** into a single, intuitive interface. It's not about replacing existing tools - it's about making them accessible through natural language, reducing cognitive load, and focusing on what matters: building great software.

---

**Start building smarter, not harder.** Give it a try and see how natural language can transform your development workflow! 🚀
