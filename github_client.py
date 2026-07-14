import httpx
import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
}

async def fetch_pr_diff(pr_info: dict) -> str:
    repo = pr_info["repo"]
    pr_number = pr_info["pr_number"]

    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/files"

    load_dotenv()
    token = os.getenv("GITHUB_TOKEN")
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        files = response.json()

    print(f"GitHub response: {files}")

    if isinstance(files, dict) and "message" in files:
        raise Exception(f"GitHub API error: {files['message']}")

    diff_text = ""
    for file in files:
        filename = file["filename"]
        patch = file.get("patch", "")
        diff_text += f"\n--- {filename} ---\n{patch}\n"

    return diff_text


async def post_pr_comment(pr_info: dict, body: str):
    repo = pr_info["repo"]
    pr_number = pr_info["pr_number"]

    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"

    load_dotenv()
    token = os.getenv("GITHUB_TOKEN")
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json={"body": body})

    if response.status_code == 201:
        print("Comment posted successfully on GitHub!")
    else:
        print(f"Failed to post comment: {response.status_code} - {response.text}")
