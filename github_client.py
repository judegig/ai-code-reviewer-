import httpx
import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
}

def parse_patch_to_numbered_lines(patch: str) -> str:
    lines = patch.splitlines()
    result = []
    new_line_num = 0
    
    for line in lines:
        if line.startswith("@@"):
            # Parse header, e.g., @@ -20,3 +20,4 @@
            parts = line.split(" ")
            if len(parts) >= 3:
                new_info = parts[2] # "+20,4" or "+20"
                if "," in new_info:
                    new_line_num = int(new_info.split(",")[0].replace("+", ""))
                else:
                    new_line_num = int(new_info.replace("+", ""))
            result.append(line)
        elif line.startswith("+"):
            result.append(f"Line {new_line_num}: {line}")
            new_line_num += 1
        elif line.startswith("-"):
            # Skip deleted lines entirely so the AI doesn't review or get confused by removed code/secrets
            continue
        else:
            # Context line (starts with space or empty)
            result.append(f"Line {new_line_num}: {line}")
            new_line_num += 1
            
    return "\n".join(result)


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
        numbered_patch = parse_patch_to_numbered_lines(patch)
        diff_text += f"\n--- {filename} ---\n{numbered_patch}\n"

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
