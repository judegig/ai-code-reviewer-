import asyncio
from main import review_pr

# Info about the test PR on your GitHub repository
pr_info = {
    "repo": "judegig/jude-portfolio",
    "pr_number": 1,
    "sha": ""
}

async def main():
    print("Starting full end-to-end code review pipeline test...")
    print("1. Fetching diff from GitHub")
    print("2. Running 4 AI agents in parallel (Linter, Security, Logic, Tests)")
    print("3. Deduplicating and grouping issues via Coordinator")
    print("4. Posting consolidated comment back to GitHub PR #1")
    print("--------------------------------------------------")
    
    await review_pr(pr_info)
    
    print("--------------------------------------------------")
    print("Pipeline test completed! Check GitHub PR #1 for the posted comment.")

if __name__ == "__main__":
    asyncio.run(main())
