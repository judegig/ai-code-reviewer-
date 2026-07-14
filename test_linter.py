import asyncio
from github_client import fetch_pr_diff
from agents.linter import linter_agent

pr_info = {
    "repo": "judegig/jude-portfolio",
    "pr_number": 1,
    "sha": ""
}

async def main():
    print("Step 1: Fetching diff from GitHub...")
    diff = await fetch_pr_diff(pr_info)
    print("Diff fetched successfully.")
    print("---")
    print(diff)
    print("---")

    print("Step 2: Sending diff to Grok for linting...")
    result = await linter_agent(diff)

    print("Step 3: Grok responded with:")
    print(result)

asyncio.run(main())
