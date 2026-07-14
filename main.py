import asyncio
from fastapi import FastAPI, Request, BackgroundTasks

from github_client import fetch_pr_diff, post_pr_comment
from agents.linter import linter_agent
from agents.security import security_agent
from agents.logic import logic_agent
from agents.tests import tests_agent
from agents.coordinator import coordinate

app = FastAPI()

SEVERITY_EMOJI = {"high": "🔴", "medium": "🟡", "low": "🟢"}


async def review_pr(pr_info: dict):
    diff = await fetch_pr_diff(pr_info)

    linter_result, security_result, logic_result, tests_result = await asyncio.gather(
        linter_agent(diff),
        security_agent(diff),
        logic_agent(diff),
        tests_agent(diff),
    )

    all_issues = (
        linter_result.get("issues", [])
        + security_result.get("issues", [])
        + logic_result.get("issues", [])
        + tests_result.get("issues", [])
    )

    # Pass through coordinator: removes duplicates, sorts, groups by file.
    grouped = coordinate(all_issues)

    # Build Markdown comment.
    if not grouped:
        comment = "## AI Code Review\n\nNo issues found. Looks good! ✅"
    else:
        total = sum(len(v) for v in grouped.values())
        lines = [f"## AI Code Review — {total} issue(s) found\n"]
        for filename, issues in grouped.items():
            lines.append(f"### `{filename}`")
            for issue in issues:
                emoji = SEVERITY_EMOJI.get(issue["severity"], "⚪")
                lines.append(f"- {emoji} **Line {issue['line']}**: {issue['message']}")
            lines.append("")
        comment = "\n".join(lines)

    await post_pr_comment(pr_info, comment)


@app.post("/webhook")
async def github_webhook(request: Request, background_tasks: BackgroundTasks):
    payload = await request.json()

    if payload.get("action") not in ("opened", "synchronize"):
        return {"status": "ignored"}

    pr_info = {
        "repo": payload["repository"]["full_name"],
        "pr_number": payload["pull_request"]["number"],
        "sha": payload["pull_request"]["head"]["sha"],
    }

    print(f"New PR received: {pr_info}")

    background_tasks.add_task(review_pr, pr_info)

    return {"status": "processing"}
