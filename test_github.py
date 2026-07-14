import asyncio
from github_client import fetch_pr_diff

pr_info = {
    "repo": "judegig/jude-portfolio",
    "pr_number": 1,
    "sha": ""
}

async def main():
    print("Fetching PR diff from GitHub...")
    diff = await fetch_pr_diff(pr_info)
    print("Here is the diff:")
    print(diff)

asyncio.run(main())
