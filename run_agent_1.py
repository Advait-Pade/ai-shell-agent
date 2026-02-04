import time

start_time = time.time()

def run_shell(command: str):
    import subprocess
    return subprocess.check_output(command, shell=True).decode()

# def web_search(query: str, max_results: int = 5):
#     from duckduckgo_search import DDGS

#     results = []
#     with DDGS() as ddgs:
#         for r in ddgs.text(query, max_results=max_results):
#             results.append(
#                 f"- {r['title']}\n  {r['href']}\n  {r['body']}"
#             )

#     return "\n\n".join(results)

SYSTEM_PROMPT = """
You are an autonomous AI agent.

You can reason step by step and decide when to use available tools
to accomplish the user's request.

Use tools when needed as tool_calls. Otherwise, answer normally.
"""


import requests
import json
import pprint

API_URL = "http://192.168.0.192:8000/v1/chat/completions"


messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": "List all the files and folders in the current directory windows system"},
    # {"role": "user", "content": "What is the capital of India"}
]

tools = [{
    "type": "function",
    "function": {
        "name": "shell",
        "description": "Run a shell command",
        "parameters": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "Shell command to execute"
                }
            },
            "required": ["command"]
        }
    }
}]

while True:
    response = requests.post(
        API_URL,
        json={
            "model" : "mistralai/Mistral-7B-Instruct-v0.3",
            "messages": messages,
            "tools" : tools,
            "tool_choice": "auto",
            "temperature": 0.1
        }
    ).json()

    # pprint.pprint(response)
    if "choices" not in response:
        print("API Error:", response)
        break

    message = response["choices"][0]["message"]
    
    if message.get('tool_calls'):
        # tool_calls = message.get("tool_calls")[0]
        for tool_calls in message.get("tool_calls"):
            tool_call_id = tool_calls['id']
            function_name = tool_calls['function']['name']
            args = json.loads(tool_calls['function']['arguments'])

            if function_name == 'shell':
                result = run_shell(args['command'])
                messages.append(message)
                messages.append({
                    'role' : "tool",
                    'tool_call_id' : tool_call_id,
                    'content' : result
                    })
    else:
        print(message['content'])
        break

print("Time taken ",round(time.time() - start_time))