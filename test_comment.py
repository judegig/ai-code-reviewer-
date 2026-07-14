import asyncio
from github_client import post_pr_comment

pr_info = {
    "repo": "judegig/jude-portfolio",
    "pr_number": 1,
    "sha": ""
}

async def main():
    print("Posting comment to GitHub PR...")
    await post_pr_comment(pr_info, "Hello from my AI code reviewer! This is a test comment.")
    print("Done.")

asyncio.run(main())
