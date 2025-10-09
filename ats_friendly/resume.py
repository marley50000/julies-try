# ats_friendly/resume.py
from jinja2 import Environment, FileSystemLoader
import os
from user_data import user_data

def generate_ats_resume():
    """Generates the ATS-friendly resume."""
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('ats_friendly/resume.html')

    rendered_resume = template.render(user_data)

    with open("ats_friendly_resume.html", "w") as f:
        f.write(rendered_resume)

    print("ATS-friendly resume generated successfully!")
