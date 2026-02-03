import time

start_time = time.time()

def run_shell(command: str):
    import subprocess
    return subprocess.check_output(command, shell=True).decode()

def web_search(query: str, max_results: int = 5):
    from duckduckgo_search import DDGS

    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results):
            results.append(
                f"- {r['title']}\n  {r['href']}\n  {r['body']}"
            )

    return "\n\n".join(results)


SYSTEM_PROMPT = """
You are an autonomous AI agent.

You can:
- Think step by step
- Decide whether to use a tool
- Call tools using JSON

TOOLS:
shell(command): run a shell command

If you want to use a tool, respond with:
{
    "tool": "shell",
    "tool_call_id" : "0abcdDEF1",
    "command": "ls -la"
}
{
    "tool": "web_search",
    "tool_call_id" : "0abcdDEF1",
    "query": ""
}

Otherwise, give a final answer.
"""

import requests
import json
import pprint

API_URL = "http://192.168.0.192:8000/v1/chat/completions"

messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    # {"role": "user", "content": "List all the files and folders in the current directory windows system"},
    {"role": "user", "content": "What is the capital of India"}
]

while True:
    response = requests.post(
        API_URL,
        json={
            "model": "Mistral-7B-v0.3",
            "messages": messages,
            "temperature": 0.1
        }
    ).json()

    # pprint.pprint(response)
    if "choices" not in response:
        print("API Error:", response)
        break

    message = response["choices"][0]["message"]
    content = message['content']
    print(content)
    try:
        tool_content = json.loads(content)
        # print(tool_content)
        if tool_content['tool'] == 'shell':
            result = run_shell(tool_content["command"])
            # print(result)
            messages.append(message)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_content['tool_call_id'],
                "content": result
            })
    except Exception as e:
        print(e)
        break

print("Time taken ",round(time.time() - start_time))