# 🍴 MealDB Interactive Recipe Platform

A comprehensive Flask web application for discovering, searching, and managing recipes with advanced features like meal recommendation, category browsing, and shopping list generation using the TheMealDB API.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)
![API](https://img.shields.io/badge/API-TheMealDB-yellow.svg)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-yellow.svg)

## ✨ Features

- 🔍 **Advanced Search** - Find recipes by meal name with instant results
- 📂 **Category Browsing** - Explore meals organized by cuisine and category
- 🎯 **Meal Details** - Complete recipe information with ingredients and instructions
- 🛒 **Smart Shopping List** - Generate and manage shopping lists from recipes
- ⭐ **Featured Meals** - Homepage carousel with popular meal recommendations
- 📱 **Fully Responsive** - Mobile, tablet, and desktop optimization
- 🎨 **Modern UI/UX** - Intuitive navigation with smooth interactions
- 💾 **Dynamic Content** - Real-time data fetching and rendering

## 🏗️ Project Structure

```
Task 08/
├── README.md                           # Project documentation
├── app.py                              # Flask application main file
├── models/                             # Pre-trained model files
│   ├── coco.names                      # COCO dataset classes
│   ├── yolov3.cfg                      # YOLOv3 configuration
│   └── yolov3.weights                  # Pre-trained weights (in .gitignore)
├── static/                             # Static assets
│   ├── app.js                          # Main application logic
│   ├── style.css                       # Complete styling
│   └── uploads/                        # Upload directory (if needed)
└── templates/                          # HTML templates
    ├── index.html                      # Homepage with featured meals
    ├── search.html                     # Search results page
    ├── meal.html                       # Detailed meal view
    ├── categories.html                 # All categories listing
    ├── category_meals.html             # Meals in selected category
    ├── browse.html                     # Browse and filter meals
    └── shopping_list.html              # Shopping list management
```

## 🚀 Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser
- Internet connection (for API access)

### Installation Steps

1. **Clone or download the project**

2. **Navigate to Task 08 directory**
   ```bash
   cd Task\ 08
   ```

3. **Install required packages**
   ```bash
   pip install flask requests
   ```

4. **Start the Flask server**
   ```bash
   python app.py
   ```

5. **Access the application**
   ```
   http://localhost:5000
   ```

## 📡 API Endpoints & Integration

### TheMealDB API Used

The application integrates with TheMealDB's free public API:

#### Search Endpoints
- **Search Meal**: `https://www.themealdb.com/api/json/v1/1/search.php?s={meal_name}`
- **Get Meal by ID**: `https://www.themealdb.com/api/json/v1/1/lookup.php?i={meal_id}`
- **Search by First Letter**: `https://www.themealdb.com/api/json/v1/1/search.php?f={letter}`

#### Category Endpoints
- **Get All Categories**: `https://www.themealdb.com/api/json/v1/1/list.php?c=list`
- **Get Meals by Category**: `https://www.themealdb.com/api/json/v1/1/filter.php?c={category}`

## 🎯 Core Features Explained

### Homepage (index.html)
- Featured meal carousel
- Search box for quick recipe lookup
- Category shortcuts
- Browse and shopping list navigation

### Search Functionality (search.html)
- Real-time meal search results
- Thumbnail images and meal details
- Quick link to full recipe
- No results handling with helpful messages

### Meal Details (meal.html)
- Complete recipe information
- Ingredient list with measurements
- Step-by-step cooking instructions
- Meal image and category info
- Add to shopping list button
- Related meals suggestions

### Category Browser (categories.html)
- List of all meal categories
- Category descriptions
- Click to view all meals in category

### Category View (category_meals.html)
- All meals in selected category
- Grid/list view options
- Thumbnail preview images
- Quick meal preview
- Add to shopping list option

### Browse (browse.html)
- Browse all available meals
- Filter and sort options
- Advanced search criteria
- Meal preview cards
- Save favorites

### Shopping List (shopping_list.html)
- Manage ingredient lists
- Add/remove items
- Organize by category
- Print list option
- Share functionality

## 💻 Frontend Technology

### HTML Templates
- Semantic HTML5 structure
- Templating with Jinja2
- Mobile-responsive design
- Accessibility features

### CSS Styling (style.css)
- Modern responsive grid layout
- Flexbox utilities
- Mobile-first approach
- Dark theme compatible
- Smooth animations and transitions
- Custom color scheme

### JavaScript (app.js)
- Dynamic content loading
- API request handling
- Event listeners and handlers
- Shopping list management
- Local storage integration
- Form validation

## 🔄 Application Flow

```
User Access
    ↓
Home Page (Featured Meals)
    ↓
├─ Search Route → Recipe Results → Meal Details
├─ Categories → Category Meals → Meal Details
├─ Browse → All Meals → Meal Details
└─ Shopping List → Manage Items
    ↓
View Recipe & Ingredients
    ↓
Add to Shopping List / Save / Share
```

## 📦 Dependencies

```
Flask>=2.3.0
requests>=2.31.0
```

## ⚙️ Configuration

### Flask App Configuration

```python
- Port: 5000
- Debug: False (set to True for development)
- Host: localhost (0.0.0.0 for network access)
```

### API Configuration

- **Base URL**: `https://www.themealdb.com/api/json/v1/1/`
- **Rate Limit**: No official limit (fair usage expected)
- **Response Format**: JSON
- **Authentication**: None (public API)

## 🔐 Data Privacy

- No user data is stored
- API calls are stateless
- No cookies or tracking
- Local storage only for shopping list (client-side)

## 🌟 Usage Examples

### Search for a Recipe
1. Enter meal name in search box
2. View results with images
3. Click on meal to see full recipe

### Create Shopping List
1. View meal details
2. Click "Add to Shopping List"
3. View shopping_list page
4. Manage ingredients
5. Print or share list

### Browse by Category
1. Go to Categories page
2. Select desired category
3. Browse meals in that category
4. Click meal for details

## 📝 Notes

- All recipe data is from TheMealDB (third-party API)
- No meal data is stored in database
- Real-time data fetching ensures up-to-date recipes
- Images are hosted by TheMealDB
- Works offline for already-loaded recipes only

## 🚧 Future Enhancements

- User authentication and favorites
- Recipe ratings and reviews
- Dietary/allergy filters
- Nutritional information
- Recipe sharing on social media
- Dark/light theme toggle
- Multiple language support
- Local recipe storage/caching

## 📄 License

MIT License - Open source for educational use

## 👨‍💻 Developer Notes

- Clean code with proper function documentation
- Modular design for easy maintenance
- Error handling for API failures
- Responsive design tested on multiple devices
- Performance optimized for fast loading

---

**Last Updated**: March 2026  
**Version**: 1.0.0
