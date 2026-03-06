// Location Mode Handler
const locationModeRadios = document.querySelectorAll('input[name="locationMode"]');
locationModeRadios.forEach(radio => {
    radio.addEventListener('change', (e) => {
        const mode = e.target.value;
        const manualInput = document.getElementById('manualLocationInput');
        const autoInfo = document.getElementById('autoLocationInfo');
        const getLocationBtn = document.getElementById('getLocationBtn');
        
        if (mode === 'auto') {
            manualInput.style.display = 'none';
            autoInfo.style.display = 'block';
            getLocationBtn.style.display = 'none';
        } else {
            manualInput.style.display = 'flex';
            autoInfo.style.display = 'none';
            getLocationBtn.style.display = 'block';
        }
    });
});

document.getElementById('uploadForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const fileInput = document.getElementById('mediaFile');
    const file = fileInput.files[0];
    
    if (!file) {
        alert('Please select a file');
        return;
    }
    
    const locationMode = document.querySelector('input[name="locationMode"]:checked').value;
    let latitude, longitude;
    
    showSpinner();
    
    // Auto mode: get location first
    if (locationMode === 'auto') {
        try {
            const position = await new Promise((resolve, reject) => {
                if (navigator.geolocation) {
                    navigator.geolocation.getCurrentPosition(resolve, reject);
                } else {
                    reject(new Error('Geolocation not supported'));
                }
            });
            latitude = position.coords.latitude;
            longitude = position.coords.longitude;
        } catch (error) {
            hideSpinner();
            alert('Could not get your location: ' + error.message + '\n\nPlease switch to Manual mode or check your browser permissions.');
            return;
        }
    } else {
        // Manual mode: use entered values
        latitude = document.getElementById('latitude').value;
        longitude = document.getElementById('longitude').value;
    }
    
    const formData = new FormData();
    formData.append('file', file);
    formData.append('latitude', latitude);
    formData.append('longitude', longitude);
    
    try {
        const response = await fetch('/api/detect', {
            method: 'POST',
            body: formData
        });
        
        hideSpinner();
        
        // Check if response is ok
        if (!response.ok) {
            const contentType = response.headers.get('content-type');
            let errorMsg = 'Error processing file. Server returned status ' + response.status;
            
            if (contentType && contentType.includes('application/json')) {
                try {
                    const data = await response.json();
                    errorMsg = data.error || errorMsg;
                } catch (e) {
                    // Response is not JSON
                }
            }
            alert(errorMsg);
            return;
        }
        
        let data;
        try {
            data = await response.json();
        } catch (jsonError) {
            console.error('Failed to parse response as JSON:', jsonError);
            alert('Error: Server returned invalid response. Check console for details.');
            return;
        }
        
        if (data.success) {
            displayResults(data, file.type);
            updateStats();
        } else {
            alert('Error: ' + data.error);
        }
    } catch (error) {
        hideSpinner();
        alert('Error processing file: ' + error.message);
    }
});

// Store latest detection data for export
let latestDetectionData = null;

// Species icons mapping
const speciesIcons = {
    'deer': '🦌',
    'elephant': '🐘',
    'lion': '🦁',
    'tiger': '🐅',
    'bear': '🐻',
    'zebra': '🦓',
    'giraffe': '🦒',
    'horse': '🐴',
    'cow': '🐄',
    'sheep': '🐑',
    'dog': '🐕',
    'cat': '🐈',
    'bird': '🦅',
    'unknown': '🐾'
};

function displayResults(data, fileType) {
    const resultsSection = document.getElementById('resultsSection');
    latestDetectionData = data;
    
    document.getElementById('animalCount').textContent = data.animal_count || data.detections || 0;
    
    // Display dominant species
    const dominant = data.dominant_species || 'N/A';
    document.getElementById('dominantSpecies').textContent = dominant.charAt(0).toUpperCase() + dominant.slice(1);
    
    // Display herd density with color
    const density = data.herd_density || 'Low';
    const densityEl = document.getElementById('herdDensity');
    densityEl.textContent = density;
    densityEl.className = 'density-' + density.toLowerCase();
    
    // Display confidence
    const confidence = data.confidence || 0.85;
    document.getElementById('confidenceScore').textContent = (confidence * 100).toFixed(1) + '%';
    
    // Display detection method with icon
    const method = data.detection_method || 'UNKNOWN';
    let methodDisplay = method;
    if (method === 'YOLO') {
        methodDisplay = '🔬 YOLO v3';
    } else if (method === 'CASCADE') {
        methodDisplay = '🔍 Cascade';
    }
    document.getElementById('detectionMethod').textContent = methodDisplay;
    
    document.getElementById('detectionTime').textContent = new Date(data.timestamp).toLocaleString();
    
    // Display species breakdown
    displaySpeciesBreakdown(data.species_breakdown);
    
    // Display location info
    displayLocationInfo(data.location);
    
    if (fileType.startsWith('image')) {
        document.getElementById('imageContainer').style.display = 'block';
        document.getElementById('videoContainer').style.display = 'none';
        document.getElementById('resultImage').src = data.image_path;
        
        // Setup download button
        const downloadBtn = document.getElementById('downloadImage');
        if (downloadBtn) {
            downloadBtn.href = data.image_path;
            downloadBtn.download = 'animal_detection_result.jpg';
        }
    } else if (fileType.startsWith('video')) {
        document.getElementById('imageContainer').style.display = 'none';
        document.getElementById('videoContainer').style.display = 'block';
        document.getElementById('resultVideo').src = data.video_path;
        
        // Setup download button
        const downloadBtn = document.getElementById('downloadVideo');
        if (downloadBtn) {
            downloadBtn.href = data.video_path;
            downloadBtn.download = 'animal_detection_result.mp4';
        }
    }
    
    if (data.map) {
        document.getElementById('mapContainer').innerHTML = data.map;
    }
    
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

function displaySpeciesBreakdown(speciesBreakdown) {
    const grid = document.getElementById('speciesGrid');
    if (!grid) return;
    
    grid.innerHTML = '';
    
    if (!speciesBreakdown || Object.keys(speciesBreakdown).length === 0) {
        grid.innerHTML = '<div class="species-item"><span class="species-icon">🐾</span><div class="species-name">No Species</div><div class="species-count">0</div></div>';
        return;
    }
    
    for (const [species, count] of Object.entries(speciesBreakdown)) {
        const icon = speciesIcons[species.toLowerCase()] || speciesIcons['unknown'];
        const item = document.createElement('div');
        item.className = 'species-item';
        item.innerHTML = `
            <span class="species-icon">${icon}</span>
            <div class="species-name">${species}</div>
            <div class="species-count">${count}</div>
        `;
        grid.appendChild(item);
    }
}

function displayLocationInfo(location) {
    const latEl = document.getElementById('resultLat');
    const lngEl = document.getElementById('resultLng');
    
    if (latEl && lngEl && location) {
        latEl.textContent = location.lat ? location.lat.toFixed(6) : 'N/A';
        lngEl.textContent = location.lng ? location.lng.toFixed(6) : 'N/A';
    }
}

function analyzeAnother() {
    document.getElementById('resultsSection').style.display = 'none';
    document.getElementById('mediaFile').value = '';
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function exportResults() {
    if (!latestDetectionData) {
        alert('No detection results to export');
        return;
    }
    
    const report = {
        title: 'Animal Herd Detection Report',
        generated_at: new Date().toISOString(),
        detection: {
            animal_count: latestDetectionData.animal_count,
            dominant_species: latestDetectionData.dominant_species,
            herd_density: latestDetectionData.herd_density,
            confidence: latestDetectionData.confidence,
            detection_method: latestDetectionData.detection_method,
            species_breakdown: latestDetectionData.species_breakdown
        },
        location: latestDetectionData.location,
        timestamp: latestDetectionData.timestamp
    };
    
    const blob = new Blob([JSON.stringify(report, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `animal_detection_report_${Date.now()}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

function updateStats() {
    fetch('/api/stats')
        .then(response => response.json())
        .then(data => {
            document.getElementById('statTotal').textContent = data.total_files;
            document.getElementById('statImages').textContent = data.images;
            document.getElementById('statVideos').textContent = data.videos;
        });
}

function showSpinner() {
    document.getElementById('loadingSpinner').style.display = 'flex';
}

function hideSpinner() {
    document.getElementById('loadingSpinner').style.display = 'none';
}

document.getElementById('getLocationBtn').addEventListener('click', () => {
    if (navigator.geolocation) {
        document.getElementById('getLocationBtn').disabled = true;
        document.getElementById('getLocationBtn').innerHTML = '<i class="fas fa-spinner fa-spin"></i> Getting location...';
        
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;
                
                document.getElementById('latitude').value = lat.toFixed(4);
                document.getElementById('longitude').value = lon.toFixed(4);
                
                document.getElementById('getLocationBtn').disabled = false;
                document.getElementById('getLocationBtn').innerHTML = '<i class="fas fa-map-marker-alt"></i> Get Current Location';
                alert(`📍 Location updated: ${lat.toFixed(4)}, ${lon.toFixed(4)}`);
            },
            (error) => {
                document.getElementById('getLocationBtn').disabled = false;
                document.getElementById('getLocationBtn').innerHTML = '<i class="fas fa-map-marker-alt"></i> Get Current Location';
                alert('Could not get location: ' + error.message);
            }
        );
    } else {
        alert('Geolocation is not supported by your browser');
    }
});

window.addEventListener('load', () => {
    updateStats();
});
