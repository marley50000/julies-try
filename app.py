from flask import Flask, render_template
from user_data import user_data

app = Flask(__name__)

@app.route('/')
def index():
    return """
    <h1>Resume and Cover Letter Generator</h1>
    <ul>
        <li><a href="/ats-resume">ATS-Friendly Resume</a></li>
        <li><a href="/ats-cover-letter">ATS-Friendly Cover Letter</a></li>
        <li><a href="/modern-canadian-resume">Modern Canadian Resume</a></li>
        <li><a href="/modern-canadian-cover-letter">Modern Canadian Cover Letter</a></li>
    </ul>
    """

@app.route('/ats-resume')
def ats_resume():
    return render_template('ats_friendly/resume.html', **user_data)

@app.route('/ats-cover-letter')
def ats_cover_letter():
    return render_template('ats_friendly_cover_letter/cover_letter.html', **user_data)

@app.route('/modern-canadian-resume')
def modern_canadian_resume():
    return render_template('modern_canadian/resume.html', **user_data)

@app.route('/modern-canadian-cover-letter')
def modern_canadian_cover_letter():
    return render_template('modern_canadian_cover_letter/cover_letter.html', **user_data)

if __name__ == '__main__':
    app.run(debug=True)
