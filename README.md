# Gemini File Agent

This project reproduces the agent described in [Practical Guide on how to build an Agent from scratch with Gemini 3](https://www.philschmid.de/building-agents).

## Setup

1. Create a virtual environment (optional but recommended) and install the dependency:
   ```bash
   pip install -r requirements.txt
   ```
2. Export your Gemini API key (create one at https://aistudio.google.com/app/apikey).
   ```bash
   export GEMINI_API_KEY=your-key
   ```

## Usage

Run the interactive agent loop:
```bash
python3 agent.py
```

The agent loads three built-in filesystem tools (`read_file`, `write_file`, `list_dir`) and responds with Gemini 3 Pro Preview while role-playing Linus Torvalds. Ask it to inspect the repository or modify files; type `exit` to quit.
