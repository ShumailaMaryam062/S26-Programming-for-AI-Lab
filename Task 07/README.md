# 🍽️ MealDB Recipe Explorer

A feature-rich Flask web application for discovering and exploring recipes using the TheMealDB API. Browse meals by category, search for recipes, and view detailed ingredient information.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)
![API](https://img.shields.io/badge/API-TheMealDB-yellow.svg)
![License](https://img.shields.io/badge/License-MIT-blue.svg)

## ✨ Features

- 🔍 **Recipe Search** - Find meals by name instantly
- 📂 **Browse by Category** - Explore meals organized by cuisine type
- 📜 **Detailed Recipes** - View complete ingredients and cooking instructions
- 📱 **Responsive Design** - Works seamlessly on desktop and mobile devices
- 🎨 **Modern UI** - Clean interface with intuitive navigation
- ⭐ **Featured Meals** - Discover popular meals on the homepage
- 🛒 **Shopping List** - Generate shopping lists from recipes
- 💾 **Recipe Details** - Full ingredient lists with measurements

## 🏗️ Project Structure

```
Task 07/
├── README.md                    # Project documentation
├── app.py                       # Flask application main file
├── models/                      # API model files
│   ├── coco.names              # COCO dataset class names
│   ├── yolov3.cfg              # YOLOv3 model configuration
│   └── yolov3.weights          # Pre-trained weights (in .gitignore)
├── static/                      # Static files
│   ├── style.css               # Application styling
│   └── script.js               # Client-side JavaScript
└── templates/                   # HTML templates
    ├── index.html              # Homepage with featured meals
    ├── search.html             # Search results page
    ├── meal.html               # Detailed meal view
    ├── categories.html         # Category browser
    ├── category_meals.html     # Meals in selected category
    ├── browse.html             # Browse all meals
    └── shopping_list.html      # Shopping list generator
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Internet connection (for API calls)

### Setup

1. **Clone or download the project**

2. **Navigate to Task 07 directory**
   ```bash
   cd Task\ 07
   ```

3. **Install dependencies**
   ```bash
   pip install flask requests
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open in browser**
   ```
   http://localhost:5000
   ```

## 📡 API Integration

### TheMealDB API Endpoints

The application uses the following TheMealDB API endpoints:

- **Search by Name**: `https://www.themealdb.com/api/json/v1/1/search.php?s=<meal_name>`
- **Get by ID**: `https://www.themealdb.com/api/json/v1/1/lookup.php?i=<meal_id>`
- **Search by Letter**: `https://www.themealdb.com/api/json/v1/1/search.php?f=<letter>`
- **List Categories**: `https://www.themealdb.com/api/json/v1/1/list.php?c=list`
- **Filter by Category**: `https://www.themealdb.com/api/json/v1/1/filter.php?c=<category>`

## 🔧 Core Functions

### Search Functionality
- Real-time recipe search by meal name
- Displays results with thumbnail images
- Shows meal ID, category, and cuisine info

### Category Management
- Browse all available meal categories
- Filter meals by selected category
- View multiple meals per category

### Recipe Details
- Complete ingredient lists with measurements
- Step-by-step cooking instructions
- Meal images and category information
- Area/cuisine information

### Shopping List
- Extract ingredients from selected meals
- Generate consolidated shopping list
- Display quantities and measurements

## 🎨 Frontend Implementation

### Pages

1. **Index (Home)** - Featured meals carousel
2. **Search** - Dynamic recipe search with results
3. **Meal Detail** - Full recipe information
4. **Categories** - All meal categories
5. **Browse** - Browse all meals
6. **Shopping List** - Generate shopping needs

### Styling

- Responsive CSS layout
- Mobile-first design approach
- Dark theme option available
- Clean typography and spacing

## 🔌 Dependencies

```
Flask==2.3.0
requests==2.31.0
```

## 📝 Notes

- All meal data is fetched from TheMealDB (free API)
- No authentication required
- Rate limiting may apply for high-frequency requests
- Internet connection required for API calls
- Data is not cached (fresh data on each request)

## 🌟 Future Features

- Local recipe caching
- User favorites/bookmarks
- Recipe ratings and reviews
- Dietary filter options
- Nutrition information display
- Recipe sharing functionality

## 📄 License

MIT License - Feel free to use for educational purposes
