# 📧 Email Scrapper

A professional web-based email extraction tool built with Flask and Python. Extract emails from any website instantly with a beautiful, modern UI.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

- 🔍 **Single URL Scraping** - Extract emails from any website
- 📋 **Bulk Extraction** - Process multiple URLs at once
- 📊 **Excel Export** - Download results as formatted Excel files
- 🎨 **Modern UI** - Beautiful dark theme with glassmorphism effects
- ⚡ **Fast & Reliable** - Efficient scraping with error handling
- 📱 **Responsive Design** - Works on desktop and mobile

## 🚀 Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

### Setup

1. **Clone or download the project**

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open in browser**
   ```
   http://localhost:20002
   ```

## 📦 Dependencies

```
flask
requests
beautifulsoup4
argparse
socid-extractor
openpyxl
```

## 🖥️ Usage

### Single URL Scraping

1. Enter a website URL in the input field
2. Click "Start Scraping"
3. View extracted emails in the results section
4. Click "Export to Excel" to download

### Multiple URLs Scraping

1. Switch to "Multiple URLs" tab
2. Enter URLs (one per line)
3. Click "Scrape All URLs"
4. View results for each URL
5. Export all results to Excel

## 📁 Project Structure

```
TheScrapper/
├── app.py                 # Flask application
├── TheScrapper.py         # CLI version (optional)
├── requirements.txt       # Python dependencies
├── modules/
│   ├── scrapper.py        # Web scraping logic
│   └── info_reader.py     # Email extraction
├── static/
│   ├── style.css          # Styling
│   └── script.js          # Frontend logic
├── templates/
│   └── index.html         # Main page
└── output/                # Excel exports
```

## 🎨 Screenshots

The application features:
- Dark theme with animated gradient background
- Glassmorphism card effects
- Stats cards showing extraction summary
- Beautiful result cards with hover animations
- Responsive design for all screen sizes

## ⚙️ Configuration

### Change Port

Edit `app.py` and modify the port number:
```python
app.run(debug=True, host='0.0.0.0', port=20002)
```

### Production Mode

For production, disable debug mode:
```python
app.run(debug=False, host='0.0.0.0', port=20002)
```

## 📝 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main web interface |
| `/api/scrape` | POST | Scrape single URL |
| `/api/scrape-multiple` | POST | Scrape multiple URLs |
| `/api/export-excel` | POST | Generate Excel file |
| `/api/download/<filename>` | GET | Download Excel file |

## 🔧 Troubleshooting

### SSL Certificate Errors
If you encounter SSL errors, the application automatically handles them by disabling certificate verification for scraping.

### Module Not Found
Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Port Already in Use
Change the port number in `app.py` or kill the process using the port.

## 👩‍💻 Author

**Made by Shumaila** - 2026

## 📄 License

This project is open source and available under the MIT License.

---

⭐ If you found this project helpful, please give it a star!
