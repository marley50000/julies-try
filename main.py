# main.py
from user_data import user_data
from ats_friendly.resume import generate_ats_resume
from ats_friendly_cover_letter.cover_letter import generate_ats_cover_letter
from modern_canadian.resume import generate_modern_canadian_resume
from modern_canadian_cover_letter.cover_letter import generate_modern_canadian_cover_letter

def main():
    """Generates all resume and cover letter versions."""
    print("Welcome to the resume and cover letter generator!")

    # Generate the ATS-friendly versions
    generate_ats_resume()
    generate_ats_cover_letter()

    # Generate the Modern Canadian versions
    generate_modern_canadian_resume()
    generate_modern_canadian_cover_letter()

    print("All documents generated successfully!")

if __name__ == "__main__":
    main()
