# modern_canadian_cover_letter/cover_letter.py
from jinja2 import Environment, FileSystemLoader
import os
from user_data import user_data

def generate_modern_canadian_cover_letter():
    """Generates the Modern Canadian cover letter."""
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('modern_canadian_cover_letter/cover_letter.html')

    rendered_cover_letter = template.render(user_data)

    with open("modern_canadian_cover_letter.html", "w") as f:
        f.write(rendered_cover_letter)

    print("Modern Canadian cover letter generated successfully!")
