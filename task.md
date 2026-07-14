# AI Code Reviewer - Task Tracker

## Done
- [x] Installed Python 3.14
- [x] Installed required packages (fastapi, uvicorn, httpx, anthropic, python-dotenv)
- [x] Created project folder `ai-code-reviewer`
- [x] Created `main.py` — FastAPI app with webhook endpoint that receives GitHub PR events
- [x] Tested webhook locally — server received fake PR payload and responded correctly
- [x] Created `.env` file — stores GitHub token and Anthropic API key securely
- [x] Created `.gitignore` file — prevents secrets and temp files from being uploaded to GitHub
- [x] Created `github_client.py` — connects to GitHub API and fetches the PR diff
- [x] Created GitHub Personal Access Token
- [x] Created test repo branch `test-pr` on `judegig/jude-portfolio`
- [x] Opened PR #1 with intentional bad code (`password = "abc123"`) for testing
- [x] Tested `github_client.py` — successfully fetched real diff from GitHub PR #1
- [x] Created `agents/linter.py` — sends diff to Groq AI and gets back a list of code issues
- [x] Tested linter agent — Groq correctly caught the hardcoded password as high severity
- [x] Tested posting a real comment on PR #1 — comment appeared successfully on GitHub

### Day 5 — Build 3 more agents + run all 4 in parallel
- [x] Created `agents/security.py` — AI agent that looks for security issues (hardcoded secrets, SQL injection, missing auth checks)
- [x] Created `agents/logic.py` — AI agent that looks for logic errors (off-by-one errors, missing null checks, wrong conditions, unhandled edge cases)
- [x] Created `agents/tests.py` — AI agent that checks if new functions have test coverage
- [x] Updated `main.py` to run all 4 agents at the same time using `asyncio.gather`

### Day 6 — Coordinator + nice formatting
- [x] Created `agents/coordinator.py` — removes duplicates, sorts by severity (high first), groups issues by file
- [x] Updated `main.py` to pass all issues through coordinator before posting comment
- [x] Comment now renders as Markdown with severity emojis (🔴 🟡 🟢) and grouped by filename
- [x] Tested coordinator with `test_coordinator.py` — deduplication, sorting, and grouping all working correctly

## To Do

### Day 7 — Polish and deploy
- [x] Write `test_full_pipeline.py` — fetches real diff from PR #1, runs all 4 agents, posts formatted Markdown comment to GitHub
- [x] Test the full end-to-end flow on a real PR and confirm comment appears on GitHub
- [x] Deploy to Render so the server runs 24/7 and not just on your laptop
- [x] Point the GitHub webhook to the live Render URL
- [x] Write a README explaining what the project does



