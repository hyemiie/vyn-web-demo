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
    print('repository received')

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            repo_url = data.get('repo_url')
            print("Request URL:", repo_url)

            if not repo_url:
                return JsonResponse({"error": "No repository URL provided."}, status=400)

            scan_result = clone_and_scan_repo(repo_url)
            print("Scan result:", scan_result)

            if isinstance(scan_result, str) and (
                scan_result.startswith("Failed") or "error" in scan_result.lower()
            ):
                return JsonResponse({"error": scan_result}, status=400)

            if scan_result:
                return JsonResponse({"report": scan_result})
            else:
                return JsonResponse({"error": "Scan failed."}, status=500)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON."}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Unexpected server error: {str(e)}"}, status=500)

    return HttpResponse("Send a POST request with a repo_url.")


def clone_and_scan_repo(repo_url):
    print('Scan attempt')
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            print(f"Cloning into: {temp_dir}")
            result = subprocess.run(
                ['git', 'clone', '--depth', '1', repo_url, temp_dir],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            print('Cloned successfully')
            scan_result = scan(target=temp_dir, format='json', recursive=True)
            print('Scan result:', scan_result)
            return scan_result

    except subprocess.CalledProcessError as e:
        error_output = e.stderr.decode()
        print("Clone error:", error_output)

        if " not found" in error_output or "Authentication" in error_output:
            return "The repository is private or does not exist."
        elif "RPC failed" in error_output or "early EOF" in error_output or "fetch-pack" in error_output:
            return "The repository is too large or network issues occurred during clone."
        else:
            return f"Failed to clone repository: {error_output.strip()}"

    except Exception as e:
        print("Unexpected error:", str(e))
        return f"Unexpected error occurred: {str(e)}"


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


