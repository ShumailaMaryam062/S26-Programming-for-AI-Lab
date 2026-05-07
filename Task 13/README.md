# CareerPath ATS Studio

CareerPath ATS Studio is a Flask-based resume analysis platform for Backend Engineer Intern and Machine Learning Engineer Intern preparation. It extracts resume text, scores it with an LLM, finds skill gaps, recommends career paths using a local knowledge base, and generates a professional PDF report.

## Features
- PDF/DOCX resume upload
- ATS scoring with breakdown
- Resume improvement suggestions
- Skill gap analysis
- RAG-based career path recommendation
- Learning roadmap generation
- Downloadable PDF report
- Persistent saved analysis

## Tech Stack
- Flask
- Vanilla JavaScript
- HTML/CSS
- Python resume parsing with `pypdf` and `python-docx`
- LLM API integration via `requests`
- PDF report generation with `reportlab`

## Project Flow
1. User uploads resume.
2. Resume text is extracted.
3. ATS score is generated.
4. Improvements and skill gaps are produced.
5. Career paths are recommended using retrieved KB context.
6. Learning roadmap is generated.
7. Final report is exported to PDF.

## Folder Structure
- `routes/` Flask routes
- `rag/` retrieval logic
- `prompts/` system prompts and schemas
- `reports/` PDF report generation
- `resume/` resume parsing
- `utils/` helper functions
- `database/` local persistence
- `templates/` HTML
- `static/` CSS and JS
- `kb/` career knowledge base

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Create `.env` with:
   - `GROK_API_KEY`
   - `GROK_API_URL` or `GROK_BASE_URL`
   - `GROK_MODEL`
3. Run:
   ```bash
   python app.py
   ```
4. Open `http://127.0.0.1:5000/`

## Viva Summary
- Why modular: each part has one responsibility.
- Why RAG: career paths use local KB context, not only raw resume text.
- Why JSON outputs: easy UI rendering and PDF generation.
- Why PDF report: full analysis can be shown and submitted as evidence.

