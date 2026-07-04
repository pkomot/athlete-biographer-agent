"""Beyond the Track — athlete lifestyle biographer agent.

Built on LangChain (langchain-anthropic) with Claude's server-side web
search tool. The search runs on Anthropic's infrastructure, so the agent
needs no separate search-provider API key — only ANTHROPIC_API_KEY.
"""

from __future__ import annotations

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage

from .prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE

MODEL_ID = "claude-opus-4-8"

# Anthropic server-side web search tool (with dynamic filtering).
# Passed through to the API verbatim by langchain-anthropic.
WEB_SEARCH_TOOL = {
    "type": "web_search_20260209",
    "name": "web_search",
    "max_uses": 15,
}

# Server-side tools run in a server loop capped at ~10 iterations per
# request; when the cap is hit the API returns stop_reason "pause_turn"
# and we must resend to let it resume.
MAX_CONTINUATIONS = 5


class BeyondTheTrackBiographer:
    """Profiles athletes as people, not stat sheets."""

    def __init__(self, model: str = MODEL_ID, max_searches: int = 15):
        tool = dict(WEB_SEARCH_TOOL, max_uses=max_searches)
        llm = ChatAnthropic(
            model=model,
            max_tokens=16000,
            thinking={"type": "adaptive"},
        )
        self._llm = llm.bind_tools([tool])

    def profile(self, athlete_name: str) -> str:
        """Research an athlete and return the formatted profile text."""
        messages: list[BaseMessage] = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=USER_PROMPT_TEMPLATE.format(athlete_name=athlete_name)),
        ]

        response = self._llm.invoke(messages)
        for _ in range(MAX_CONTINUATIONS):
            if response.response_metadata.get("stop_reason") != "pause_turn":
                break
            # Resume the paused server-tool turn: replay the assistant
            # content as-is, with no extra user message.
            messages.append(response)
            response = self._llm.invoke(messages)

        return _extract_text(response)


def _extract_text(message: BaseMessage) -> str:
    """Join the text blocks of a response, skipping tool-use blocks."""
    content = message.content
    if isinstance(content, str):
        return content
    parts = [
        block["text"]
        for block in content
        if isinstance(block, dict) and block.get("type") == "text"
    ]
    return "".join(parts)
