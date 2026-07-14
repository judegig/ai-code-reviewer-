# AI Code Reviewer

## Overview
This project is an AI-powered GitHub Pull Request (PR) Code Reviewer. When a developer submits new code changes to GitHub as a Pull Request, this system automatically fetches the changes (the diff), runs four specialized AI agents in parallel to review the code, and posts a consolidated, organized review comment directly on the GitHub PR.

## Architecture & Flow
1. **Webhook Trigger**: GitHub sends a webhook payload to the FastAPI server (`/webhook`) when a PR is opened or updated.
2. **Fetch Diff**: The server uses `github_client.py` to fetch the code changes from the GitHub REST API.
3. **Parallel AI Review**: `main.py` uses `asyncio.gather` to send the diff to four AI agents concurrently:
   - **Linter Agent**: Checks for style issues, unused imports, and bad variable naming.
   - **Security Agent**: Checks for hardcoded secrets, SQL injection risks, and missing auth checks.
   - **Logic Agent**: Checks for bugs, off-by-one errors, and unhandled edge cases.
   - **Tests Agent**: Checks if new functions/classes have corresponding test coverage.
4. **Data Sanitization**: The raw JSON output from the Groq (Llama-3.3) API is sanitized using `clean_and_parse_json` in `agents/utils.py` to automatically fix Markdown blocks or AI syntax errors.
5. **Coordination**: `agents/coordinator.py` removes duplicate issues, sorts them by severity (High 🔴 -> Medium 🟡 -> Low 🟢), and groups them by filename.
6. **Post Feedback**: `github_client.py` formats the organized issues into Markdown and posts a comment back to the GitHub PR.

## Tech Stack
- **Backend Framework**: FastAPI (Python)
- **AI Integration**: Groq API (Llama-3.3-70b-versatile model) via OpenAI Python SDK
- **Concurrency**: Python `asyncio` for executing parallel API requests.
- **GitHub Integration**: GitHub REST API (using the `httpx` library) for fetching diffs and posting comments.
- **Configuration**: `python-dotenv` for securely managing secrets (`GITHUB_TOKEN`, `GROK_API_KEY`).

## Directory Structure
- `main.py`: Entry point for the FastAPI server and the core review orchestration logic.
- `github_client.py`: Handles all communication with the GitHub API.
- `agents/`
  - `linter.py`, `security.py`, `logic.py`, `tests.py`: The specialized AI reviewer agents.
  - `coordinator.py`: Merges, deduplicates, and sorts the AI feedback.
  - `utils.py`: Contains robust JSON parsing logic to safely handle raw LLM outputs.
- `test_full_pipeline.py`: An integration test script that runs the entire end-to-end flow on PR #1 manually without needing a webhook trigger.
- `task.md`: The project task tracker and progress log.
- `memory.md`: Developer guidelines, constraints, and overarching project goals.

## How to Test Locally
You can run the full end-to-end pipeline locally to test the integration. This downloads the latest code from PR #1, analyzes it with all 4 agents, and posts a review back to GitHub:

```powershell
py test_full_pipeline.py
```

To test individual components:
- `py test_coordinator.py`: Tests deduplication, sorting, and grouping logic locally.
- `py test_github.py`: Tests the GitHub connection by fetching the PR diff.
- `py test_linter.py`: Tests a single AI agent by sending it a diff and printing the response.
