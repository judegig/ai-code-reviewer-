# AI Code Reviewer

An automated, real-time AI code review assistant. When code changes are submitted to GitHub in a Pull Request (PR), this system automatically intercepts the changes via a webhook, runs four specialized AI agents in parallel to review the code, and publishes a consolidated, organized review comment directly on the PR.

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Llama3.3](https://img.shields.io/badge/Llama_3.3-Groq-orange?style=for-the-badge)
![Render](https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)

---

## 🚀 Key Features

* **Multi-Agent Architecture**: Uses 4 specialized AI agents working concurrently to evaluate code changes:
  * **Linter Agent**: Analyzes code formatting, naming conventions, and style inconsistencies.
  * **Security Agent**: Scans for hardcoded secrets, SQL injection risks, and authorization gaps.
  * **Logic Agent**: Looks for bugs, off-by-one errors, infinite loops, and edge case failures.
  * **Tests Agent**: Checks test coverage for new additions.
* **Concurrent Execution**: Orchestrated using Python’s native `asyncio.gather`, executing all 4 LLM requests in parallel to reduce processing latency by over 70%.
* **Smart Coordination**: A central coordinator deduplicates overlapping findings, ranks them by severity, and groups them by exact file paths to ensure clean, readable reports.
* **Pinpoint Accuracy**: Agents are strictly constrained to only report issues on modified lines, eliminating false positives from surrounding context code.
* **Resilient Parsing**: Custom regex-based sanitization parsing automatically extracts and formats JSON responses even when LLMs output surrounding text.
* **Real-time Automation**: Connected to GitHub Webhooks to run automatically whenever a PR is created or updated.

---

## 🛠️ Tech Stack

* **Backend**: FastAPI (Python)
* **LLM Engine**: Llama-3.3-70b-versatile (via Groq API)
* **Libraries**: `openai`, `httpx`, `python-dotenv`, `uvicorn`
* **Infrastructure**: Git, GitHub Webhooks, Render (cloud hosting)

---

## 📁 File Structure

* `main.py` — Webhook handler and coordinator execution.
* `github_client.py` — Pulls git diffs and posts markdown comments to GitHub APIs.
* `agents/` — Sub-agents folder containing:
  * `linter.py`, `security.py`, `logic.py`, `tests.py` — Reviewer agents.
  * `coordinator.py` — Deduplication and sorting logic.
  * `utils.py` — Custom JSON sanitizer.
* `test_full_pipeline.py` — End-to-end local integration test script.

---

## 💻 Setup & Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/YOUR_GITHUB_USERNAME/ai-code-reviewer-.git
   cd ai-code-reviewer-
   ```

2. **Configure Environment Variables**:
   Create a `.env` file in the root folder:
   ```env
   GITHUB_TOKEN=your_github_personal_access_token
   GROK_API_KEY=your_groq_api_key
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Locally**:
   ```bash
   uvicorn main:app --reload
   ```

---

## 📈 Testing
Run the manual integration test to verify the connection and agents:
```bash
py test_full_pipeline.py
```
