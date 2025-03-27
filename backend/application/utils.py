from jinja2 import Template
import requests

def format_report(html_template, data):
    with open(html_template) as file:
        template = Template(file.read())
        # Allow both dictionary with 'data' key and direct parameter passing
        if isinstance(data, dict) and 'data' not in data:
            return template.render(**data)
        return template.render(data=data)

def fetch_user_data():
    url = "http://localhost:8025/api/v2/users/jim"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API Failed with status code {response.status_code}: {response.text}")