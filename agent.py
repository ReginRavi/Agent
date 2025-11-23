"""Minimal Gemini 3 powered agent inspired by https://www.philschmid.de/building-agents.

Enhanced with 24 tools organized into specialized modules:
- file_ops: File operations (5 tools)
- git_ops: Git workflow (6 tools)
- code_analysis: Code quality (3 tools)
- network_ops: Network & web (4 tools)
- environment: System & packages (6 tools)
"""

from __future__ import annotations

import os
from typing import Any

from google import genai
from google.genai import types

from tools import ALL_TOOLS


class Agent:
    """Stateful wrapper around the Gemini 3 API."""

    def __init__(
        self,
        model: str,
        tools: dict[str, dict[str, Any]],
        *,
        system_instruction: str = "You are a helpful assistant.",
    ) -> None:
        self.model = model
        self.client = genai.Client()
        self.contents: list[dict[str, Any]] = []
        self.tools = tools
        self.system_instruction = system_instruction

    def run(
        self, contents: str | list[dict[str, Any]]
    ) -> types.GenerateContentResponse:
        """Send either plain text or function responses and return the reply."""
        if isinstance(contents, list):
            self.contents.append({"role": "user", "parts": contents})
        else:
            self.contents.append({"role": "user", "parts": [{"text": contents}]})

        config = types.GenerateContentConfig(
            system_instruction=self.system_instruction,
            tools=[
                types.Tool(
                    function_declarations=[
                        tool["definition"] for tool in self.tools.values()
                    ]
                )
            ],
        )

        response = self.client.models.generate_content(
            model=self.model,
            contents=self.contents,
            config=config,
        )
        self.contents.append(response.candidates[0].content)

        if response.function_calls:
            function_response_parts: list[dict[str, Any]] = []
            for tool_call in response.function_calls:
                tool_name = tool_call.name
                if tool_name not in self.tools:
                    result = {"error": f"Tool '{tool_name}' not found."}
                else:
                    tool_fn = self.tools[tool_name]["function"]
                    result = {"result": tool_fn(**tool_call.args)}

                function_response_parts.append(
                    {
                        "functionResponse": {
                            "name": tool_name,
                            "response": result,
                        }
                    }
                )

            return self.run(function_response_parts)

        return response


def main() -> None:
    if "GEMINI_API_KEY" not in os.environ:
        raise RuntimeError("Set GEMINI_API_KEY before running the agent.")

    agent = Agent(
        model="gemini-2.5-flash",
        tools=ALL_TOOLS,
        system_instruction="You are a helpful coding assistant. Respond like Linus Torvalds.",
    )

    print("🤖 Enhanced Gemini Agent - Developer Edition v3.0")
    print("=" * 55)
    print("📦 44 Tools Available:")
    print("  • File Ops: read, write, delete, append, find/replace")
    print("  • Directory Ops: list, create, search, file info")
    print("  • Git: status, diff, log, add, commit, branch, pull, push,")
    print("         stash, remote")
    print("  • Code Analysis: analyze, find TODOs, count LOC")
    print("  • Data: JSON, CSV, YAML read/write/query")
    print("  • Text Utils: regex, formatting, base64 encode/decode")
    print("  • Archives: create/extract/list zip files")
    print("  • Network: web search, HTTP requests")
    print("  • System: execute commands, processes, resource stats")
    print("  • Environment: info, package management")
    print("=" * 55)
    print("Type 'exit' to quit.\n")
    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break

        if not user_input:
            continue
        if user_input.lower() in {"exit", "quit"}:
            break

        response = agent.run(user_input)
        text = getattr(response, "text", "").strip()
        print(f"Linus: {text or '[no text returned]'}\n")


if __name__ == "__main__":
    main()
