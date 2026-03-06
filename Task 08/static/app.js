// ============================================
// FAVORITES / BOOKMARKS
// ============================================

function toggleFavorite(mealId, mealName) {
    let favorites = JSON.parse(localStorage.getItem('spiceSphere_favorites')) || [];
    const index = favorites.findIndex(fav => fav.id === mealId);
    
    const btn = document.getElementById('favBtn');
    
    if (index > -1) {
        favorites.splice(index, 1);
        btn.classList.remove('active');
        btn.innerHTML = '<i class="fas fa-heart"></i> Add to Favorites';
        showNotification('Removed from Favorites', 'info');
    } else {
        favorites.push({ id: mealId, name: mealName, date: new Date().toISOString() });
        btn.classList.add('active');
        btn.innerHTML = '<i class="fas fa-heart"></i> Saved to Favorites';
        showNotification('Added to Favorites!', 'success');
    }
    
    localStorage.setItem('spiceSphere_favorites', JSON.stringify(favorites));
}

function checkFavorite(mealId) {
    let favorites = JSON.parse(localStorage.getItem('spiceSphere_favorites')) || [];
    const btn = document.getElementById('favBtn');
    
    if (favorites.some(fav => fav.id === mealId)) {
        btn.classList.add('active');
        btn.innerHTML = '<i class="fas fa-heart"></i> Saved to Favorites';
    }
}

// ============================================
// SHOPPING LIST
// ============================================

function addToShoppingList() {
    let shoppingList = JSON.parse(localStorage.getItem('spiceSphere_shopping')) || [];
    const ingredients = document.querySelectorAll('.ingredient-item');
    let addedCount = 0;
    
    ingredients.forEach(item => {
        const measure = item.querySelector('.ingredient-measure').textContent;
        const name = item.querySelector('.ingredient-name').textContent;
        const ingredient = { measure, name, checked: false };
        
        if (!shoppingList.some(item => item.name === name)) {
            shoppingList.push(ingredient);
            addedCount++;
        }
    });
    
    localStorage.setItem('spiceSphere_shopping', JSON.stringify(shoppingList));
    showNotification(`Added ${addedCount} ingredients to Shopping List!`, 'success');
}

function viewShoppingList() {
    window.location.href = '/shopping-list';
}

// ============================================
// PRINT RECIPE
// ============================================

function printRecipe() {
    const mealTitle = document.querySelector('.meal-title').textContent;
    const printWindow = window.open('', '', 'width=900,height=600');
    
    const ingredients = Array.from(document.querySelectorAll('.ingredient-item'))
        .map(item => `<li>${item.querySelector('.ingredient-measure').textContent} ${item.querySelector('.ingredient-name').textContent}</li>`)
        .join('');
    
    const instructions = Array.from(document.querySelectorAll('.instruction-step .step-text'))
        .map((step, idx) => `<p><strong>Step ${idx + 1}:</strong> ${step.textContent}</p>`)
        .join('');
    
    const html = `
        <!DOCTYPE html>
        <html>
        <head>
            <title>${mealTitle}</title>
            <style>
                body { font-family: Arial, sans-serif; padding: 40px; color: #333; }
                h1 { color: #FF006E; font-size: 36px; margin-bottom: 10px; }
                h2 { color: #00F5FF; font-size: 22px; margin-top: 30px; border-bottom: 2px solid #00F5FF; padding-bottom: 10px; }
                ul { padding-left: 25px; }
                li { margin: 8px 0; }
                p { line-height: 1.8; margin: 10px 0; }
                .meta { color: #666; margin: 20px 0; font-size: 14px; }
                @media print { body { padding: 0; } }
            </style>
        </head>
        <body>
            <h1>${mealTitle}</h1>
            <div class="meta">Printed from SpiceSphere</div>
            <h2>Ingredients</h2>
            <ul>${ingredients}</ul>
            <h2>Instructions</h2>
            ${instructions}
        </body>
        </html>
    `;
    
    printWindow.document.write(html);
    printWindow.document.close();
    setTimeout(() => printWindow.print(), 250);
}

// ============================================
// SERVINGS ADJUSTER
// ============================================

function adjustServings(multiplier) {
    const ingredients = document.querySelectorAll('.ingredient-item');
    const servingBtn = document.getElementById('servingCount');
    let currentServings = parseInt(servingBtn.textContent) || 1;
    const newServings = Math.max(1, currentServings + multiplier);
    const ratio = newServings / currentServings;
    
    ingredients.forEach(item => {
        const measure = item.querySelector('.ingredient-measure');
        const text = measure.getAttribute('data-original') || measure.textContent;
        measure.setAttribute('data-original', text);
        
        let newMeasure = text;
        const match = text.match(/^([\d.]+)\s*(.*)$/);
        
        if (match) {
            const number = parseFloat(match[1]) * ratio;
            const unit = match[2];
            newMeasure = `${number.toFixed(1)} ${unit}`;
        }
        
        measure.textContent = newMeasure;
    });
    
    servingBtn.textContent = newServings;
}

// ============================================
// RATING SYSTEM
// ============================================

function setRating(stars) {
    const mealId = document.querySelector('[data-meal-id]').getAttribute('data-meal-id');
    let ratings = JSON.parse(localStorage.getItem('spiceSphere_ratings')) || {};
    
    ratings[mealId] = stars;
    localStorage.setItem('spiceSphere_ratings', JSON.stringify(ratings));
    
    updateRatingDisplay(stars);
    showNotification(`You rated this recipe ${stars} ⭐`, 'success');
}

function updateRatingDisplay(rating) {
    const stars = document.querySelectorAll('.rating-star');
    stars.forEach((star, idx) => {
        if (idx < rating) {
            star.classList.add('active');
        } else {
            star.classList.remove('active');
        }
    });
}

function loadRating(mealId) {
    let ratings = JSON.parse(localStorage.getItem('spiceSphere_ratings')) || {};
    const savedRating = ratings[mealId] || 0;
    updateRatingDisplay(savedRating);
}

// ============================================
// NOTIFICATIONS
// ============================================

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `<i class="fas fa-check-circle"></i> ${message}`;
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        padding: 16px 24px;
        background: ${type === 'success' ? '#00FF87' : '#00F5FF'};
        color: #0A0A0F;
        border-radius: 30px;
        font-weight: 700;
        z-index: 1000;
        animation: slideIn 0.3s ease-out;
        box-shadow: 0 0 20px ${type === 'success' ? 'rgba(0, 255, 135, 0.5)' : 'rgba(0, 245, 255, 0.5)'};
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 2500);
}

// ============================================
// INITIALIZATIONS
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    const mealIdElement = document.querySelector('[data-meal-id]');
    if (mealIdElement) {
        const mealId = mealIdElement.getAttribute('data-meal-id');
        checkFavorite(mealId);
        loadRating(mealId);
    }
});

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
