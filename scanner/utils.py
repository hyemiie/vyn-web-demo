import os
import click
import requests
from .bandit_test import run_bandit_on_path
from .analyzer import get_ai_suggestion, save_scan_report
from prettytable import PrettyTable

def scan(target, format, recursive):
    print(f" Scanning {target}...\n")

    if not os.path.exists(target):
        return f'The path {target} does not exist.'
    
    issue_list = []

    if os.path.isdir(target):
        if recursive:
            for root, _, files in os.walk(target):
                for file in files:
                    if file.endswith(".py"):
                        full_path = os.path.join(root, file)
                        issue_list.extend(run_bandit_on_path(full_path))
        else:
            message = f"Skipping directory ({target}), use --recursive or -r to scan contents"
            print(message)
            return message
    else:
        issue_list = run_bandit_on_path(target)

    if not issue_list:
        return "No Python issues found."

    report_text = ""

    if format == 'table':
        table = PrettyTable()
        table.field_names = ["File", "Line", "Issue", "Severity", "Confidence", "AI Suggestion"]

    for result in issue_list:
        issue = result.as_dict()
        issue_details = (
            "=" * 50 + "\n" +
            f"→ Issue      : {issue['issue_text']}\n" +
            f"→ File       : {issue['filename']}\n" +
            f"→ Line       : {issue['line_number']}\n" +
            f"→ Severity   : {issue['issue_severity']}\n" +
            f"→ Confidence : {issue['issue_confidence']}\n"
        )

        code_context = issue.get('code', "Code not available")
        # try:
        #     response =  get_ai_suggestion(issue_text= issue['issue_text'], code_snippet= code_context)
        #     print('response', response)
        #     if response.status_code == 200:
        #         suggestion = response.json()
        #         ai_suggestion = suggestion.get('content', 'No suggestion returned')
        #     else:
        #         ai_suggestion = f"AI request failed: {response.status_code} {response.text}"
        # except Exception as e:
        #     ai_suggestion = f"AI request error: {str(e)}"
        try:
            ai_suggestion = get_ai_suggestion(issue_text=issue['issue_text'], code_snippet=code_context)
            print('response', ai_suggestion)        
        except Exception as e:
            ai_suggestion = f"AI request error: {str(e)}"

        issue_details += f"→ AI Suggestion: {ai_suggestion}\n"

        if format == 'table':
            table.add_row([
                issue['filename'],
                issue['line_number'],
                issue['issue_text'],
                issue['issue_severity'],
                issue['issue_confidence'],
                ai_suggestion
            ])
        else:
            print(issue_details)

        report_text += issue_details + "\n"

    if format == 'table':
        print(table)

    return report_text
