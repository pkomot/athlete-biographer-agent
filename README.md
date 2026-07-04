# Beyond the Track 🏃‍♀️✨

An AI biographer agent that profiles athletes as **people, not stat sheets**.
Give it a name, and it researches the human behind the athlete — childhood
roots, hobbies, fashion, philanthropy, and online vibe — then writes a warm,
magazine-style profile.

Built with **Python + LangChain** (`langchain-anthropic`) on **Claude Opus 4.8**,
using Anthropic's server-side **web search** tool, so no separate search-provider
API key is needed.

## How it works

1. **Professional context (baseline)** — confirms discipline and standing via
   World Athletics / regional bodies, briefly.
2. **The human element (focus)** — digs into news archives and features for
   human-interest stories.
3. **Social & lifestyle (the vibe)** — public social media insights, interviews,
   fashion, travel, family life.
4. **Community & impact** — philanthropy, business ventures, mentorship,
   activism.

The output is structured into five sections: ⚡ The Elevator Pitch ·
🌍 Roots & Reality · 🎨 Passions & Play · ❤️ Heart & Hustle · 📱 The Social Radar.

Race times, tactical breakdowns, injury histories, and training regimes are
deliberately filtered out (unique training locations like Iten, Kenya are
mentioned for their lifestyle angle only).

## Setup

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
```

## Usage

CLI:

```bash
python -m beyond_the_track "Faith Kipyegon"
```

Options:

- `--model` — Claude model id (default `claude-opus-4-8`)
- `--max-searches` — cap on web searches per profile (default 15)

As a library:

```python
from beyond_the_track import BeyondTheTrackBiographer

biographer = BeyondTheTrackBiographer()
print(biographer.profile("Eliud Kipchoge"))
```

## Project layout

```
beyond_the_track/
  agent.py      # LangChain agent: Claude + server-side web search, pause_turn handling
  prompts.py    # System prompt: retrieval strategy, filtering rules, output sections, tone
  __main__.py   # CLI entry point
requirements.txt
```

## Notes

- A profile takes a minute or two — the agent runs a multi-layered search
  strategy (typically 8–15 web searches) before writing.
- The system prompt lives in `beyond_the_track/prompts.py`; tweak the tone,
  sections, or filtering rules there.
- The agent handles the API's `pause_turn` stop reason automatically (the
  server-side search loop can pause on long research runs and must be resumed).
