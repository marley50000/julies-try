from flask import Flask, render_template, request, make_response, url_for
from weasyprint import HTML, CSS
import collections
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def parse_dynamic_fields(form_data, prefix):
    """Parses dynamically added form fields (e.g., work_experience, education)."""
    items = []
    grouped_by_index = collections.defaultdict(dict)
    for key, value in form_data.items():
        if key.startswith(prefix):
            parts = key.split('-')
            index = int(parts[1])
            field_name = parts[2]
            grouped_by_index[index][field_name] = value

    sorted_indices = sorted(grouped_by_index.keys())
    for index in sorted_indices:
        items.append(grouped_by_index[index])
    return items

@app.route('/')
def homepage():
    """Renders the new homepage with a template gallery."""
    return render_template('homepage.html')

@app.route('/form/<template_name>')
def show_form(template_name):
    """Renders the main form, pre-selecting the template."""
    return render_template('index.html', selected_template=template_name)

@app.route('/generate', methods=['POST'])
def generate():
    """Generates the selected document as a downloadable PDF."""
    form_data = request.form.to_dict()
    document_type = form_data.get('document_type')

    photo_path = None
    if 'passport_photo' in request.files:
        photo = request.files['passport_photo']
        if photo.filename != '':
            filename = secure_filename(photo.filename)
            save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), app.config['UPLOAD_FOLDER'], filename)

            os.makedirs(os.path.dirname(save_path), exist_ok=True)

            photo.save(save_path)
            photo_path = url_for('static', filename=f'uploads/{filename}')

    context = {
        "name": form_data.get('name'),
        "contact_info": {
            "email": form_data.get('email'),
            "phone": form_data.get('phone'),
            "linkedin": form_data.get('linkedin'),
            "github": form_data.get('github'),
        },
        "career_summary": form_data.get('career_summary'),
        "job_target": form_data.get('job_target'),
        "date": form_data.get('date'),
        "hiring_manager_name": form_data.get('hiring_manager_name'),
        "company_name": form_data.get('company_name'),
        "company_address": form_data.get('company_address'),
        "skills": [skill.strip() for skill in form_data.get('skills', '').split(',')],
        "work_experience": parse_dynamic_fields(form_data, 'work_experience'),
        "education": parse_dynamic_fields(form_data, 'education'),
        "photo_path": photo_path,
    }

    template_map = {
        "elegant_professional_resume": "elegant_professional/resume.html",
        "modern_professional_resume": "modern_professional/resume.html",
        "ats_resume": "ats_friendly/resume.html",
        "ats_cover_letter": "ats_friendly_cover_letter/cover_letter.html",
        "modern_canadian_resume": "modern_canadian/resume.html",
        "modern_canadian_cover_letter": "modern_canadian_cover_letter/cover_letter.html",
    }

    template_name = template_map.get(document_type)
    if not template_name:
        return "Invalid document type selected.", 400

    rendered_html = render_template(template_name, **context)

    base_url = request.url_root
    pdf = HTML(string=rendered_html, base_url=base_url).write_pdf()

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename={document_type}.pdf'

    return response

if __name__ == '__main__':
    app.run(debug=True)
