import json
import subprocess
import tempfile
import os
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
import requests

from .utils import scan
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPEN_ROUTER_AI_KEY") 


@csrf_exempt
def receive_repo(request):
    print('repository recieved')
    if request.method == "POST":
        # Use .POST.get() instead of .body for form data
        repo_url = json.loads(request.body).get('repo_url')
        # print("request", json.loads(request.body).get('repo_url'))
        print("request url", repo_url)

        if not repo_url:
            return JsonResponse({"error": "No repository URL provided."}, status=400)

        scan_result = clone_and_scan_repo(repo_url)
        print('scan result', scan_result)

        if scan_result:
            return JsonResponse({
                     "report": scan_result

            })
        else:
            return JsonResponse({"error": "Scan failed."}, status=500)

    return HttpResponse("Send a POST request with a repo_url.")


def clone_and_scan_repo(repo_url):
    print('scan attempt')
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            subprocess.run(['git', 'clone', repo_url, temp_dir], check=True)
            print('cloned')
            result = scan(target=temp_dir, format='json', recursive=True)
            print('result', result)
            return result
    except subprocess.CalledProcessError as e:
        print("Error:", e)
        return None


def get_ai_suggestion(issue_text, code_snippet):
    prompt = f"""🔒 Security Issue:

Issue: {issue_text}

Code:
{code_snippet}

🔧 Suggest a concise fix (max 5 lines of code) and a 1-line explanation. Skip extra details or long best practices.
"""

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        reply = response.json()
        return reply["choices"][0]["message"]["content"]
    except Exception as e:
        return f"AI request failed: {str(e)}"


