import asyncio
from agents.coordinator import coordinate

# Fake issues list — simulates what the 4 agents might return combined.
# Notice: requirements.txt line 1 appears TWICE (duplicate) and issues are out of order.
fake_issues = [
    {"file": "requirements.txt", "line": 1, "severity": "high",   "message": "Hardcoded password detected"},
    {"file": "requirements.txt", "line": 1, "severity": "high",   "message": "Sensitive credential exposed"},  # duplicate line
    {"file": "app.py",           "line": 10, "severity": "low",    "message": "Variable name too short"},
    {"file": "app.py",           "line": 22, "severity": "medium", "message": "Missing None check before use"},
    {"file": "app.py",           "line": 5,  "severity": "high",   "message": "eval() is dangerous"},
]

grouped = coordinate(fake_issues)

print("=== Coordinator Test Results ===\n")
for filename, issues in grouped.items():
    print(f"File: {filename}")
    for issue in issues:
        print(f"  [{issue['severity'].upper()}] Line {issue['line']}: {issue['message']}")
    print()

# Count total issues after deduplication
total = sum(len(v) for v in grouped.values())
print(f"Total issues after deduplication: {total} (started with {len(fake_issues)})")
print("Duplicate removed: 1 (requirements.txt line 1 appeared twice)")
