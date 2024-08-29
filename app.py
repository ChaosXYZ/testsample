import requests
import json
from datetime import datetime
import os

def execute_api_test(url, method='GET', headers=None, params=None, data=None, validation_func=None):
    try:
        start_time = datetime.now()
        if method.upper() == 'GET':
            response = requests.get(url, headers=headers, params=params)
        elif method.upper() == 'POST':
            response = requests.post(url, headers=headers, json=data, params=params)
        elif method.upper() == 'PUT':
            response = requests.put(url, headers=headers, json=data, params=params)
        elif method.upper() == 'DELETE':
            response = requests.delete(url, headers=headers, params=params)
        else:
            return {"error": f"Unsupported method: {method}", "passed": False}

        end_time = datetime.now()
        elapsed_time = (end_time - start_time).total_seconds() * 1000  # Convert to milliseconds

        content = response.json() if response.headers.get('Content-Type') == 'application/json' else response.text
        
        result = {
            "url": url,
            "method": method,
            "params": params,
            "data": data,
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "content": content,
            "response_time": elapsed_time,
            "passed": 200 <= response.status_code < 300
        }

        if validation_func:
            validation_result = validation_func(result)
            result.update(validation_result)

        return result
    except Exception as e:
        return {"error": str(e), "passed": False}

def get_json_snippet(content, max_length=500):
    if isinstance(content, dict):
        json_str = json.dumps(content, indent=2)
        if len(json_str) <= max_length:
            return json_str
        return json_str[:max_length] + "..."
    return str(content)[:max_length] + "..."

def save_full_response(content, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as f:
        json.dump(content, f, indent=2)
    return filename

def generate_html_report(api_results):
    total_tests = sum(len(api['tests']) for api in api_results)
    passed_tests = sum(sum(1 for test in api['tests'] if test.get('passed', False)) for api in api_results)
    total_time = sum(sum(test['response_time'] for test in api['tests']) for api in api_results)

    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>API Test Report</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f4f4f4;
            }
            h1, h2, h3 {
                color: #2c3e50;
            }
            h1 {
                border-bottom: 2px solid #3498db;
                padding-bottom: 10px;
            }
            .overview {
                background-color: #ecf0f1;
                border-radius: 5px;
                padding: 15px;
                margin-bottom: 20px;
            }
            .overview-item {
                margin-bottom: 10px;
            }
            .api-group {
                background-color: white;
                border-radius: 5px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                margin-bottom: 20px;
                overflow: hidden;
            }
            .api-header {
                background-color: #3498db;
                color: white;
                padding: 10px 15px;
                cursor: pointer;
                user-select: none;
            }
            .api-content {
                display: none;
                padding: 15px;
            }
            table {
                border-collapse: collapse;
                width: 100%;
                margin-bottom: 15px;
            }
            th, td {
                border: 1px solid #ddd;
                padding: 12px;
                text-align: left;
            }
            th {
                background-color: #f2f2f2;
                font-weight: bold;
            }
            pre {
                background-color: #f8f8f8;
                border: 1px solid #ddd;
                border-radius: 3px;
                padding: 10px;
                overflow-x: auto;
                max-height: 300px;
            }
            .pass {
                background-color: #27ae60;
                color: white;
                font-weight: bold;
            }
            .fail {
                background-color: #c0392b;
                color: white;
                font-weight: bold;
            }
        </style>
        <script>
            function toggleApiContent(apiId) {
                var content = document.getElementById(apiId);
                content.style.display = content.style.display === "block" ? "none" : "block";
            }
        </script>
    </head>
    <body>
        <h1>API Test Report</h1>
        <div class="overview">
            <h2>Overview</h2>
            <div class="overview-item"><strong>Total Tests:</strong> {}</div>
            <div class="overview-item"><strong>Passed Tests:</strong> {}</div>
            <div class="overview-item"><strong>Failed Tests:</strong> {}</div>
            <div class="overview-item"><strong>Success Rate:</strong> {:.2f}%</div>
            <div class="overview-item"><strong>Total Response Time:</strong> {:.2f} ms</div>
            <div class="overview-item"><strong>Average Response Time:</strong> {:.2f} ms</div>
            <div class="overview-item"><strong>Timestamp:</strong> {}</div>
        </div>
    """.format(
        total_tests,
        passed_tests,
        total_tests - passed_tests,
        (passed_tests / total_tests) * 100 if total_tests > 0 else 0,
        total_time,
        total_time / total_tests if total_tests > 0 else 0,
        datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )

    for i, api in enumerate(api_results, 1):
        api_id = f"api-{i}"
        html += f"""
        <div class="api-group">
            <div class="api-header" onclick="toggleApiContent('{api_id}')">
                {api['name']}
            </div>
            <div id="{api_id}" class="api-content">
                <h2>Test Results</h2>
        """
        for j, result in enumerate(api['tests'], 1):
            passed = result.get('passed', False)
            pass_fail = "pass" if passed else "fail"
            html += f"""
                <h3>Test {j}: {result['name']}</h3>
                <table>
                    <tr><th>URL</th><td>{result['url']}</td></tr>
                    <tr><th>Method</th><td>{result['method']}</td></tr>
                    <tr><th>Parameters</th><td><pre>{json.dumps(result.get('params'), indent=2)}</pre></td></tr>
                    <tr><th>Data</th><td><pre>{json.dumps(result.get('data'), indent=2)}</pre></td></tr>
                    <tr><th>Status Code</th><td>{result['status_code']}</td></tr>
                    <tr><th>Response Time</th><td>{result['response_time']:.2f} ms</td></tr>
                    <tr><th>Headers</th><td><pre>{json.dumps(result['headers'], indent=2)}</pre></td></tr>
                    <tr><th>JSON Snippet</th><td><pre>{get_json_snippet(result['content'])}</pre></td></tr>
                    <tr><th>Full Response</th><td><a href="{result['full_response_file']}" target="_blank">View Full Response</a></td></tr>
                    <tr><th>Pass/Fail</th><td class="{pass_fail}">{pass_fail.upper()}</td></tr>
                </table>
            """
            if 'custom_checks' in result:
                html += "<h4>Custom Checks</h4><ul>"
                for check, check_result in result['custom_checks']:
                    html += f"<li>{check}: {'Passed' if check_result else 'Failed'}</li>"
                html += "</ul>"
        html += """
            </div>
        </div>
        """

    html += "</body></html>"
    return html

# Custom validation functions
def validate_user_api(result):
    content = result['content']
    checks = []
    
    if 'users' in content:
        checks.append(("'users' key exists", True))
        if len(content['users']) > 0:
            checks.append(("Users list is not empty", True))
            for user in content['users']:
                if 'id' in user and 'name' in user:
                    checks.append((f"User {user['id']} has 'id' and 'name'", True))
                else:
                    checks.append((f"User {user['id']} has 'id' and 'name'", False))
        else:
            checks.append(("Users list is not empty", False))
    else:
        checks.append(("'users' key exists", False))
    
    return {"custom_checks": checks, "passed": all(check[1] for check in checks)}

def validate_post_api(result):
    content = result['content']
    checks = []
    
    if 'posts' in content:
        checks.append(("'posts' key exists", True))
        if len(content['posts']) > 0:
            checks.append(("Posts list is not empty", True))
            for post in content['posts']:
                if 'id' in post and 'title' in post and 'body' in post:
                    checks.append((f"Post {post['id']} has 'id', 'title', and 'body'", True))
                else:
                    checks.append((f"Post {post['id']} has 'id', 'title', and 'body'", False))
        else:
            checks.append(("Posts list is not empty", False))
    else:
        checks.append(("'posts' key exists", False))
    
    return {"custom_checks": checks, "passed": all(check[1] for check in checks)}

# Define your API tests here
api_tests = [
    {
        "name": "User API",
        "tests": [
            {
                "name": "Get Users",
                "url": "https://api.example.com/users",
                "method": "GET",
                "params": {"page": 1, "limit": 10},
                "validation_func": validate_user_api
            },
            {
                "name": "Create User",
                "url": "https://api.example.com/users",
                "method": "POST",
                "data": {"name": "John Doe", "email": "john@example.com"},
                "validation_func": validate_user_api
            }
        ]
    },
    {
        "name": "Post API",
        "tests": [
            {
                "name": "Get Posts",
                "url": "https://api.example.com/posts",
                "method": "GET",
                "params": {"user_id": 1},
                "validation_func": validate_post_api
            },
            {
                "name": "Create Post",
                "url": "https://api.example.com/posts",
                "method": "POST",
                "data": {"title": "Test Post", "body": "This is a test post.", "user_id": 1},
                "validation_func": validate_post_api
            }
        ]
    }
]

def main():
    api_results = []
    for api in api_tests:
        api_result = {"name": api["name"], "tests": []}
        for test in api["tests"]:
            result = execute_api_test(
                test["url"],
                test["method"],
                params=test.get("params"),
                data=test.get("data"),
                validation_func=test.get("validation_func")
            )
            result["name"] = test["name"]
            if "error" not in result:
                full_response_file = f"responses/{api['name']}_{test['name'].replace(' ', '_')}.json"
                result["full_response_file"] = save_full_response(result["content"], full_response_file)
            api_result["tests"].append(result)
        api_results.append(api_result)

    report = generate_html_report(api_results)

    with open("api_test_report.html", "w") as f:
        f.write(report)

    print("API test report generated and saved to 'api_test_report.html'")
    print("Full response files saved in 'responses' directory.")

if __name__ == "__main__":
    main()