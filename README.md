
# ResumeIQ — AI-Powered Resume Analyzer & Job Matcher

ResumeIQ is a Python-based web application that helps job seekers analyze their resumes against job descriptions. It identifies matching keywords, highlights missing requirements, calculates text similarity, and generates a professionally formatted resume PDF.

## Features

- **Resume Analysis:** Upload a resume in PDF format.
- **Job Description Matching:** Compare resume content with a target job description.
- **Similarity Score:** Calculate text similarity using TF-IDF and cosine similarity.
- **Keyword Analysis:** Identify matching keywords and potentially missing requirements.
- **Resume Builder:** Enter personal, educational, skills, experience, and project details to generate a PDF resume.
- **Interactive Web Interface:** Built with Streamlit.

## Tech Stack

- Python
- Streamlit
- Scikit-learn
- TF-IDF
- Cosine Similarity
- PyMuPDF
- ReportLab

## Project Structure

```text
ResumeIQ/
├── app.py
├── resume_parser.py
├── matcher.py
├── resume_builder.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Amir87641/ResumeIQ.git
cd ResumeIQ
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the environment

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

## How It Works

1. Upload a resume in PDF format.
2. Enter the job description for the position you want.
3. Analyze the resume to view its similarity score, matching keywords, and missing keywords.
4. Use the resume builder to enter your details and generate a PDF resume.

## Limitations

- The similarity score measures text similarity; it does not guarantee job suitability or hiring success.
- Keyword matching may not understand synonyms or the full context of a requirement.
- Scanned PDFs may require OCR support to extract their text accurately.

## Future Improvements

- Improve skill extraction and semantic matching.
- Add resume feedback and actionable improvement suggestions.
- Support additional resume formats.
- Add more detailed visualizations and analysis.

## Author

GitHub: [Amir87641](https://github.com/Amir87641)
