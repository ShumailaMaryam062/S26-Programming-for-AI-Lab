from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import cv2
import numpy as np
from detection import AnimalDetector
import folium
from folium import plugins
import uuid
from datetime import datetime
import io

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov'}

detector = AnimalDetector()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_map_with_location(latitude, longitude, animal_count, image_name):
    map_obj = folium.Map(
        location=[latitude, longitude],
        zoom_start=12,
        tiles='OpenStreetMap'
    )
    
    folium.Marker(
        location=[latitude, longitude],
        popup=f'Herd Detected<br>Animals: {animal_count}',
        tooltip=f'Location: {image_name}',
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(map_obj)
    
    circle = folium.Circle(
        location=[latitude, longitude],
        radius=500,
        color='red',
        fill=True,
        fillColor='red',
        fillOpacity=0.3,
        popup=f'Herd Detection Zone'
    )
    circle.add_to(map_obj)
    
    map_html = map_obj._repr_html_()
    return map_html

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/detect', methods=['POST'])
def detect_animals():
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        file = request.files['file']
        latitude = request.form.get('latitude', 40.7128)
        longitude = request.form.get('longitude', -74.0060)
        
        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except:
            latitude = 40.7128
            longitude = -74.0060
        
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'success': False, 'error': 'File type not allowed'}), 400
        
        filename = secure_filename(file.filename)
        temp_filename = f"{uuid.uuid4()}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], temp_filename)
        
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        
        file.save(filepath)
        
        file_ext = filename.rsplit('.', 1)[1].lower()
        
        if file_ext in {'mp4', 'avi', 'mov'}:
            output_filename = f"output_{temp_filename}"
            if not output_filename.endswith('.mp4'):
                output_filename = output_filename + '.mp4'
            output_video = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
            success, detections_list, detection_method, species_count = detector.process_video(filepath, output_video)
            
            if success:
                total_animals = sum(d.get('count', 0) for d in detections_list) if detections_list else 0
                
                # Determine dominant species
                dominant_species = "N/A"
                if species_count:
                    dominant_species = max(species_count, key=species_count.get)
                
                # Calculate herd density
                herd_density = "Low" if total_animals < 5 else "Medium" if total_animals < 15 else "High"
                
                # Calculate average confidence
                avg_confidence = 0.85
                total_conf = 0
                count_conf = 0
                for detection in detections_list:
                    for member in detection.get('members', []):
                        total_conf += member.get('confidence', 0.85)
                        count_conf += 1
                if count_conf > 0:
                    avg_confidence = total_conf / count_conf
                
                map_html = generate_map_with_location(latitude, longitude, total_animals, filename)
                
                return jsonify({
                    'success': True,
                    'message': f'Detected animals in {len(detections_list)} frames',
                    'animal_count': total_animals,
                    'detections': total_animals,
                    'frames': len(detections_list),
                    'video_path': f'uploads/{os.path.basename(output_video)}',
                    'map': map_html,
                    'timestamp': datetime.now().isoformat(),
                    'detection_method': detection_method,
                    'confidence': round(avg_confidence, 4),
                    'species_breakdown': species_count,
                    'dominant_species': dominant_species,
                    'herd_density': herd_density,
                    'location': {'lat': latitude, 'lng': longitude}
                })
            else:
                return jsonify({'success': False, 'error': 'Video processing failed'}), 500
        
        else:
            result_image, detections, detection_method, species_count = detector.process_image(filepath)
            
            if result_image is None:
                return jsonify({'success': False, 'error': 'Could not process image'}), 400
            
            output_image_path = os.path.join(app.config['UPLOAD_FOLDER'], f"result_{temp_filename}")
            cv2.imwrite(output_image_path, result_image)
            
            animal_count = len(detections)
            avg_confidence = np.mean([d.get('confidence', 0.85) for d in detections]) if detections else 0
            
            # Calculate herd density based on count
            herd_density = "Low" if animal_count < 3 else "Medium" if animal_count < 8 else "High"
            
            # Determine dominant species
            dominant_species = max(species_count, key=species_count.get) if species_count else "None"
            
            map_html = generate_map_with_location(latitude, longitude, animal_count, filename)
            
            return jsonify({
                'success': True,
                'animal_count': animal_count,
                'detections': len(detections),
                'image_path': f'uploads/{os.path.basename(output_image_path)}',
                'original_image': f'uploads/{temp_filename}',
                'map': map_html,
                'timestamp': datetime.now().isoformat(),
                'detection_method': detection_method,
                'confidence': round(avg_confidence, 4),
                'species_breakdown': species_count,
                'dominant_species': dominant_species,
                'herd_density': herd_density,
                'location': {'lat': latitude, 'lng': longitude}
            })
    
    except Exception as e:
        import traceback
        error_msg = str(e)
        traceback.print_exc()
        return jsonify({
            'success': False, 
            'error': f'Error processing file: {error_msg}'
        }), 500

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))

@app.route('/api/stats')
def get_stats():
    if os.path.exists(app.config['UPLOAD_FOLDER']):
        files = os.listdir(app.config['UPLOAD_FOLDER'])
        image_files = len([f for f in files if f.endswith(('png', 'jpg', 'jpeg', 'gif'))])
        video_files = len([f for f in files if f.endswith(('mp4', 'avi', 'mov'))])
        
        return jsonify({
            'total_files': len(files),
            'images': image_files,
            'videos': video_files
        })
    
    return jsonify({
        'total_files': 0,
        'images': 0,
        'videos': 0
    })

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=3000)
