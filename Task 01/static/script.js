// Tab switching
document.querySelectorAll('.tab-button').forEach(button => {
    button.addEventListener('click', function() {
        const tabName = this.getAttribute('data-tab');
        
        // Remove active class from all buttons and contents
        document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
        
        // Add active class to clicked button and corresponding content
        this.classList.add('active');
        document.getElementById(tabName).classList.add('active');
    });
});

// Store results for export
let currentResults = [];

// Single URL Scraping
async function scrapeSingle() {
    const url = document.getElementById('url').value.trim();
    
    if (!url) {
        showNotification('Please enter a URL', 'error');
        return;
    }
    
    const loading = document.getElementById('loading');
    loading.classList.remove('hidden');
    hideResults();
    
    try {
        const response = await fetch('/api/scrape', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            showError(data.error || 'An error occurred');
            loading.classList.add('hidden');
            return;
        }
        
        displaySingleResult(data);
    } catch (error) {
        showError('Error: ' + error.message);
    } finally {
        loading.classList.add('hidden');
    }
}

// Multiple URLs Scraping
async function scrapeMultiple() {
    const urlsText = document.getElementById('urls').value.trim();
    
    if (!urlsText) {
        showNotification('Please enter at least one URL', 'error');
        return;
    }
    
    const urls = urlsText.split('\n').filter(url => url.trim());
    
    const loading = document.getElementById('loading-multiple');
    loading.classList.remove('hidden');
    hideResults();
    
    try {
        const response = await fetch('/api/scrape-multiple', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ urls })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            showError(data.error || 'An error occurred');
            loading.classList.add('hidden');
            return;
        }
        
        displayMultipleResults(data.results);
    } catch (error) {
        showError('Error: ' + error.message);
    } finally {
        loading.classList.add('hidden');
    }
}

// Display single result
function displaySingleResult(data) {
    const resultsSection = document.getElementById('results-section');
    const resultsContent = document.getElementById('results-content');
    const statsContainer = document.getElementById('stats-container');
    
    // Store for export
    currentResults = [data];
    
    // Show stats
    statsContainer.innerHTML = `
        <div class="stats-row">
            <div class="stat-card">
                <div class="number">${data.emails.length}</div>
                <div class="label">Emails Found</div>
            </div>
            <div class="stat-card">
                <div class="number">1</div>
                <div class="label">URL Scraped</div>
            </div>
        </div>
    `;
    
    let html = '';
    
    if (data.success) {
        html = `
            <div class="result-card">
                <h3>
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path d="M12 21a9.004 9.004 0 008.716-6.747M12 21a9.004 9.004 0 01-8.716-6.747M12 21c2.485 0 4.5-4.03 4.5-9S14.485 3 12 3m0 18c-2.485 0-4.5-4.03-4.5-9S9.515 3 12 3m0 0a8.997 8.997 0 017.843 4.582M12 3a8.997 8.997 0 00-7.843 4.582m15.686 0A11.953 11.953 0 0112 10.5c-2.998 0-5.74-1.1-7.843-2.918m15.686 0A8.959 8.959 0 0121 12c0 .778-.099 1.533-.284 2.253m0 0A17.919 17.919 0 0112 16.5c-3.162 0-6.133-.815-8.716-2.247m0 0A9.015 9.015 0 013 12c0-1.605.42-3.113 1.157-4.418"/></svg>
                    ${escapeHtml(data.url)}
                </h3>
                
                <div class="result-category">
                    <h4>📧 Extracted Emails (${data.emails.length})</h4>
                    ${data.emails.length > 0 ? `
                        <ul class="result-list">
                            ${data.emails.map(email => `<li>${escapeHtml(email)}</li>`).join('')}
                        </ul>
                    ` : '<p class="empty-results">No emails found on this page</p>'}
                </div>
            </div>
        `;
    } else {
        html = `
            <div class="error">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path fill-rule="evenodd" d="M9.401 3.003c1.155-2 4.043-2 5.197 0l7.355 12.748c1.154 2-.29 4.5-2.599 4.5H4.645c-2.309 0-3.752-2.5-2.598-4.5L9.4 3.003zM12 8.25a.75.75 0 01.75.75v3.75a.75.75 0 01-1.5 0V9a.75.75 0 01.75-.75zm0 8.25a.75.75 0 100-1.5.75.75 0 000 1.5z" clip-rule="evenodd"/></svg>
                ${escapeHtml(data.error)}
            </div>
        `;
    }
    
    resultsContent.innerHTML = html;
    resultsSection.classList.remove('hidden');
    document.getElementById('export-btn').style.display = data.success && data.emails.length > 0 ? 'inline-flex' : 'none';
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

// Display multiple results
function displayMultipleResults(results) {
    const resultsSection = document.getElementById('results-section');
    const resultsContent = document.getElementById('results-content');
    const statsContainer = document.getElementById('stats-container');
    
    // Store for export
    currentResults = results;
    
    // Calculate stats
    const totalEmails = results.reduce((sum, r) => sum + (r.success ? r.emails.length : 0), 0);
    const successCount = results.filter(r => r.success).length;
    
    // Show stats
    statsContainer.innerHTML = `
        <div class="stats-row">
            <div class="stat-card">
                <div class="number">${totalEmails}</div>
                <div class="label">Total Emails</div>
            </div>
            <div class="stat-card">
                <div class="number">${results.length}</div>
                <div class="label">URLs Processed</div>
            </div>
            <div class="stat-card">
                <div class="number">${successCount}</div>
                <div class="label">Successful</div>
            </div>
        </div>
    `;
    
    let html = '';
    
    results.forEach(result => {
        if (result.success) {
            html += `
                <div class="result-card">
                    <h3>
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path d="M12 21a9.004 9.004 0 008.716-6.747M12 21a9.004 9.004 0 01-8.716-6.747M12 21c2.485 0 4.5-4.03 4.5-9S14.485 3 12 3m0 18c-2.485 0-4.5-4.03-4.5-9S9.515 3 12 3m0 0a8.997 8.997 0 017.843 4.582M12 3a8.997 8.997 0 00-7.843 4.582m15.686 0A11.953 11.953 0 0112 10.5c-2.998 0-5.74-1.1-7.843-2.918m15.686 0A8.959 8.959 0 0121 12c0 .778-.099 1.533-.284 2.253m0 0A17.919 17.919 0 0112 16.5c-3.162 0-6.133-.815-8.716-2.247m0 0A9.015 9.015 0 013 12c0-1.605.42-3.113 1.157-4.418"/></svg>
                        ${escapeHtml(result.url)}
                    </h3>
                    
                    <div class="result-category">
                        <h4>📧 Extracted Emails (${result.emails.length})</h4>
                        ${result.emails.length > 0 ? `
                            <ul class="result-list">
                                ${result.emails.map(email => `<li>${escapeHtml(email)}</li>`).join('')}
                            </ul>
                        ` : '<p class="empty-results">No emails found</p>'}
                    </div>
                </div>
            `;
        } else {
            html += `
                <div class="result-card">
                    <h3>
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path d="M12 21a9.004 9.004 0 008.716-6.747M12 21a9.004 9.004 0 01-8.716-6.747M12 21c2.485 0 4.5-4.03 4.5-9S14.485 3 12 3m0 18c-2.485 0-4.5-4.03-4.5-9S9.515 3 12 3m0 0a8.997 8.997 0 017.843 4.582M12 3a8.997 8.997 0 00-7.843 4.582m15.686 0A11.953 11.953 0 0112 10.5c-2.998 0-5.74-1.1-7.843-2.918m15.686 0A8.959 8.959 0 0121 12c0 .778-.099 1.533-.284 2.253m0 0A17.919 17.919 0 0112 16.5c-3.162 0-6.133-.815-8.716-2.247m0 0A9.015 9.015 0 013 12c0-1.605.42-3.113 1.157-4.418"/></svg>
                        ${escapeHtml(result.url)}
                    </h3>
                    <div class="error">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path fill-rule="evenodd" d="M9.401 3.003c1.155-2 4.043-2 5.197 0l7.355 12.748c1.154 2-.29 4.5-2.599 4.5H4.645c-2.309 0-3.752-2.5-2.598-4.5L9.4 3.003zM12 8.25a.75.75 0 01.75.75v3.75a.75.75 0 01-1.5 0V9a.75.75 0 01.75-.75zm0 8.25a.75.75 0 100-1.5.75.75 0 000 1.5z" clip-rule="evenodd"/></svg>
                        ${escapeHtml(result.error)}
                    </div>
                </div>
            `;
        }
    });
    
    resultsContent.innerHTML = html;
    resultsSection.classList.remove('hidden');
    document.getElementById('export-btn').style.display = totalEmails > 0 ? 'inline-flex' : 'none';
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

// Show error message
function showError(message) {
    const resultsSection = document.getElementById('results-section');
    const resultsContent = document.getElementById('results-content');
    const statsContainer = document.getElementById('stats-container');
    
    statsContainer.innerHTML = '';
    resultsContent.innerHTML = `
        <div class="error">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path fill-rule="evenodd" d="M9.401 3.003c1.155-2 4.043-2 5.197 0l7.355 12.748c1.154 2-.29 4.5-2.599 4.5H4.645c-2.309 0-3.752-2.5-2.598-4.5L9.4 3.003zM12 8.25a.75.75 0 01.75.75v3.75a.75.75 0 01-1.5 0V9a.75.75 0 01.75-.75zm0 8.25a.75.75 0 100-1.5.75.75 0 000 1.5z" clip-rule="evenodd"/></svg>
            ${escapeHtml(message)}
        </div>
    `;
    resultsSection.classList.remove('hidden');
    document.getElementById('export-btn').style.display = 'none';
}

// Hide results section
function hideResults() {
    document.getElementById('results-section').classList.add('hidden');
}

// Show notification
function showNotification(message, type = 'info') {
    // Simple alert for now - could be enhanced with toast notifications
    alert(message);
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Allow Enter key for single URL input
document.getElementById('url').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        scrapeSingle();
    }
});

// Export results to Excel
async function exportToExcel() {
    if (currentResults.length === 0) {
        showNotification('No results to export', 'error');
        return;
    }
    
    const exportBtn = document.getElementById('export-btn');
    const originalContent = exportBtn.innerHTML;
    exportBtn.disabled = true;
    exportBtn.innerHTML = `
        <svg class="animate-pulse" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path fill-rule="evenodd" d="M12 2.25a.75.75 0 01.75.75v11.69l3.22-3.22a.75.75 0 111.06 1.06l-4.5 4.5a.75.75 0 01-1.06 0l-4.5-4.5a.75.75 0 111.06-1.06l3.22 3.22V3a.75.75 0 01.75-.75zm-9 13.5a.75.75 0 01.75.75v2.25a1.5 1.5 0 001.5 1.5h13.5a1.5 1.5 0 001.5-1.5V16.5a.75.75 0 011.5 0v2.25a3 3 0 01-3 3H5.25a3 3 0 01-3-3V16.5a.75.75 0 01.75-.75z" clip-rule="evenodd"/></svg>
        Generating...
    `;
    
    try {
        const response = await fetch('/api/export-excel', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ results: currentResults })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            showNotification('Error exporting: ' + (data.error || 'Unknown error'), 'error');
            return;
        }
        
        // Download the file
        window.location.href = `/api/download/${data.filename}`;
    } catch (error) {
        showNotification('Error: ' + error.message, 'error');
    } finally {
        exportBtn.disabled = false;
        exportBtn.innerHTML = originalContent;
    }
}
