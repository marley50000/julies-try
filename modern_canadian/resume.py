# modern_canadian/resume.py
from jinja2 import Environment, FileSystemLoader
import os
from user_data import user_data

def generate_modern_canadian_resume():
    """Generates the Modern Canadian resume."""
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('modern_canadian/resume.html')

    rendered_resume = template.render(user_data)

    with open("modern_canadian_resume.html", "w") as f:
        f.write(rendered_resume)

    print("Modern Canadian resume generated successfully!")
