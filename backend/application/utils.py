from jinja2 import Template

def format_report(html_template, data):
    with open(html_template) as file:
        template = Template(file.read())
        # Allow both dictionary with 'data' key and direct parameter passing
        if isinstance(data, dict) and 'data' not in data:
            return template.render(**data)
        return template.render(data=data)