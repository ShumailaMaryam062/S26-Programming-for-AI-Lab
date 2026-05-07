================================================================================
    FINDMATE - CAMPUS LOST & FOUND QnA CHATBOT
================================================================================

PROJECT DESCRIPTION:
FindMate is an intelligent Q&A chatbot that helps campus users find lost items
and report found items. It uses AI-powered semantic search to match user 
queries with relevant answers from the QnA dataset.

TECHNOLOGY STACK:
- Backend: Flask (Python web framework)
- NLP: Sentence Transformers (all-MiniLM-L6-v2 model)
- Vector Search: FAISS (Facebook AI Similarity Search)
- Frontend: HTML + CSS + JavaScript
- Data: CSV-based QnA dataset

FEATURES:
✓ Semantic similarity search for finding relevant answers
✓ Text preprocessing and cleaning
✓ Fast vector-based similarity matching
✓ Web-based chat interface
✓ Category-based answer organization
✓ Automatic embedding caching

PROJECT STRUCTURE:
├── app.py                    # Flask application
├── FindMate_QnABot.ipynb     # Jupyter notebook for testing/development
├── qna_dataset.csv           # QnA pairs (question, answer, category)
├── requirements.txt          # Python dependencies
├── static/
│   └── style.css             # CSS styling
└── templates/
    └── index.html            # Web interface

INSTALLATION & SETUP:
1. Navigate to project directory in terminal
2. Install dependencies:
   pip install -r requirements.txt

3. Run the application:
   python app.py

4. Open in browser:
   http://localhost:50009

REQUIREMENTS:
- Python 3.8+
- Flask 2.3.3
- sentence-transformers 5.3.0
- faiss-cpu 1.13.2
- pandas
- numpy

FIRST RUN:
⚠️  First run will take 2-5 minutes:
   - Downloads MiniLM model (~330MB) from Hugging Face
   - Generates embeddings for all QnA pairs
   - Creates FAISS index
   - Saves embeddings.npy and faiss.index files

✓  Subsequent runs will be instant (uses cached embeddings)
✓  Internet required only for first model download

HOW IT WORKS:
1. User enters a question in the web interface
2. Question is preprocessed (lowercased, punctuation removed)
3. MiniLM model converts question to embedding vector
4. FAISS searches for most similar QnA pairs
5. Top result is returned with answer and matched question

DATASET FORMAT (qna_dataset.csv):
question,answer,category
"I lost my ID card","📋 Check Student Affairs Office...",lost_id
"Where can I find my charger?","🔌 Check Computer Labs...",lost_charger

CUSTOMIZATION:
- Edit qna_dataset.csv to add/modify QnA pairs
- Restart app.py to regenerate embeddings
- Adjust search results count in app.py: search_findmate(query, count=3)

TROUBLESHOOTING:
Q: Connection refused at localhost:50009?
A: Make sure app.py is running. Check terminal for errors.

Q: "Module not found" errors?
A: Run: pip install -r requirements.txt

Q: Embeddings taking too long to generate?
A: Normal for first run. Check internet connection. Be patient (5 min max).

DEVELOPMENT:
- Use FindMate_QnABot.ipynb for testing new features
- Modify embedding model in app.py (MODEL_NAME variable)
- Adjust FAISS index type (currently IndexFlatL2 for Euclidean distance)

LICENSE:
Open source - Feel free to modify and distribute

AUTHOR:
FindMate Development Team
Contact: For support or suggestions, modify qna_dataset.csv and rebuild

VERSION: 1.0
Last Updated: May 2026
