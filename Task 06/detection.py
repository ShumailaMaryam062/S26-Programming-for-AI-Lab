import cv2
import numpy as np
import os
from pathlib import Path
import random

class AnimalDetector:
    ANIMAL_CLASSES = {
        'dog': {'color': (255, 128, 0), 'icon': '🐕'},
        'cat': {'color': (255, 0, 128), 'icon': '🐈'},
        'horse': {'color': (0, 128, 255), 'icon': '🐎'},
        'cow': {'color': (128, 64, 0), 'icon': '🐄'},
        'sheep': {'color': (200, 200, 200), 'icon': '🐑'},
        'goat': {'color': (150, 100, 50), 'icon': '🐐'},
        'elephant': {'color': (128, 128, 128), 'icon': '🐘'},
        'zebra': {'color': (50, 50, 50), 'icon': '🦓'},
        'giraffe': {'color': (0, 200, 255), 'icon': '🦒'},
        'lion': {'color': (0, 165, 255), 'icon': '🦁'},
        'tiger': {'color': (0, 100, 255), 'icon': '🐅'},
        'bear': {'color': (60, 40, 20), 'icon': '🐻'},
        'deer': {'color': (80, 120, 160), 'icon': '🦌'},
        'bird': {'color': (255, 200, 0), 'icon': '🐦'},
        'unknown': {'color': (0, 255, 0), 'icon': '❓'}
    }
    
    COCO_ANIMALS = {
        14: 'bird', 15: 'cat', 16: 'dog', 17: 'horse', 18: 'sheep',
        19: 'cow', 20: 'elephant', 21: 'bear', 22: 'zebra', 23: 'giraffe'
    }
    
    def __init__(self):
        self.net = None
        self.layer_names = None
        self.output_layers = None
        self.classes = None
        self.model_loaded = False
        self.detection_method = "NONE"
        self.load_yolo_model()
    
    def load_yolo_model(self):
        weights_path = "models/yolov3.weights"
        config_path = "models/yolov3.cfg"
        names_path = "models/coco.names"
        
        self.net = cv2.dnn.readNet(weights_path, config_path)
        with open(names_path, "r") as f:
            self.classes = [line.strip() for line in f.readlines()]
        
        self.layer_names = self.net.getLayerNames()
        self.output_layers = [self.layer_names[i - 1] for i in self.net.getUnconnectedOutLayers()]
        self.model_loaded = True
        self.detection_method = "YOLO"
        print("✓ YOLO model loaded successfully")
    
    def detect_animals_yolo(self, image):
        height, width, channels = image.shape
        blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        self.net.setInput(blob)
        outs = self.net.forward(self.output_layers)
        
        class_ids = []
        confidences = []
        boxes = []
        
        valid_animals = set(self.COCO_ANIMALS.keys())
        
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                
                if confidence > 0.5 and class_id in valid_animals:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = center_x - w // 2
                    y = center_y - h // 2
                    
                    if w > 15 and h > 15:
                        boxes.append([x, y, w, h])
                        confidences.append(float(confidence))
                        class_ids.append(class_id)
        
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        detections = []
        
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                class_id = class_ids[i]
                species = self.COCO_ANIMALS.get(class_id, 'unknown')
                confidence = confidences[i]
                
                detections.append({
                    'box': (x, y, w, h),
                    'confidence': confidence,
                    'class': class_id,
                    'species': species
                })
        
        return detections
    

    

    
    def process_image(self, image_path):
        image = cv2.imread(image_path)
        if image is None:
            return None, [], "ERROR"
        
        detections = self.detect_animals_yolo(image)
        
        result_image = image.copy()
        species_count = {}
        
        for i, detection in enumerate(detections):
            x, y, w, h = detection['box']
            confidence = detection.get('confidence', 0.85)
            
            if 'species' in detection:
                species = detection['species']
            elif 'class' in detection and self.classes:
                class_name = self.classes[detection['class']]
                species = class_name if class_name in self.ANIMAL_CLASSES else 'unknown'
            else:
                species = 'unknown'
            
            species_count[species] = species_count.get(species, 0) + 1
            
            color = self.ANIMAL_CLASSES.get(species, self.ANIMAL_CLASSES['unknown'])['color']
            
            cv2.rectangle(result_image, (x, y), (x + w, y + h), color, 4)
            
            species_label = f"{species.upper()}"
            count_label = f"#{species_count[species]}"
            conf_label = f"{confidence:.0%}"
            
            font_scale = 0.9
            font_thick = 3
            label_size1, _ = cv2.getTextSize(species_label, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thick)
            
            label_height = label_size1[1] + 6
            bg_height = label_height * 3 + 15
            
            label_x1 = max(0, x - 2)
            label_y1 = max(0, y - bg_height)
            label_x2 = min(result_image.shape[1], x + label_size1[0] + 12)
            label_y2 = min(result_image.shape[0], y + 4)
            
            cv2.rectangle(result_image, (label_x1, label_y1), (label_x2, label_y2), color, -1)
            cv2.rectangle(result_image, (label_x1, label_y1), (label_x2, label_y2), (0, 0, 0), 2)
            
            text_y = max(label_height + 2, label_y1 + label_height + 2)
            cv2.putText(result_image, species_label, (label_x1 + 5, text_y), 
                       cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), font_thick)
            
            cv2.putText(result_image, count_label, (label_x1 + 5, text_y + label_height), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            cv2.putText(result_image, conf_label, (label_x1 + 5, text_y + label_height * 2 - 5), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 200), 2)
            
            detection['species'] = species
        
        summary_y = 30
        cv2.putText(result_image, f"Total Animals: {len(detections)}", (10, summary_y), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        
        return result_image, detections, self.detection_method, species_count
    
    def process_video(self, video_path, output_path):
        import subprocess
        
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            print(f"❌ Cannot open video: {video_path}")
            return False, [], self.detection_method, {}
        
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        if fps <= 0:
            fps = 30
        
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        print(f"📹 Input: {width}x{height} @ {fps}fps, {total_frames} frames")
        
        temp_avi = output_path.replace('.mp4', '_raw.avi')
        output_path_final = output_path if output_path.endswith('.mp4') else output_path + '.mp4'
        
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        writer = cv2.VideoWriter(temp_avi, fourcc, fps, (width, height))
        
        if not writer.isOpened():
            print("❌ Failed to create AVI writer")
            cap.release()
            return False, [], self.detection_method, {}
        
        all_detections = []
        total_species_count = {}
        frame_count = 0
        
        print("Processing frames...")
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            detections = self.detect_animals_yolo(frame)
            
            frame_species = {}
            
            for detection in detections:
                x, y, w, h = detection['box']
                confidence = detection.get('confidence', 0.85)
                species = detection.get('species', 'unknown')
                
                frame_species[species] = frame_species.get(species, 0) + 1
                total_species_count[species] = total_species_count.get(species, 0) + 1
                
                color = self.ANIMAL_CLASSES.get(species, self.ANIMAL_CLASSES['unknown'])['color']
                cv2.rectangle(frame, (x, y), (x+w, y+h), color, 3)
                label = f"{species}: {confidence:.0%}"
                cv2.putText(frame, label, (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            
            cv2.putText(frame, f"Frame {frame_count}: {len(detections)} animals", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2)
            
            all_detections.append({
                'frame': frame_count,
                'count': len(detections),
                'species': frame_species,
                'members': [{'confidence': d.get('confidence', 0.85)} for d in detections]
            })
            
            writer.write(frame)
            frame_count += 1
            
            if frame_count % 30 == 0:
                print(f"  Processed {frame_count}/{total_frames} frames...")
        
        cap.release()
        writer.release()
        
        print(f"✓ Wrote {frame_count} frames to AVI")
        
        if os.path.exists(temp_avi):
            print(f"Converting to MP4 using FFmpeg...")
            cmd = [
                'ffmpeg',
                '-i', temp_avi,
                '-c:v', 'libx264',
                '-preset', 'fast',
                '-crf', '28',
                '-movflags', '+faststart',
                '-c:a', 'aac',
                output_path_final,
                '-y',
                '-loglevel', 'error'
            ]
            
            result = subprocess.run(cmd, capture_output=True, timeout=600)
            
            if result.returncode == 0 and os.path.exists(output_path_final):
                file_size = os.path.getsize(output_path_final)
                print(f"✓ MP4 created: {output_path_final} ({file_size/1024/1024:.1f}MB)")
                
                try:
                    os.remove(temp_avi)
                except:
                    pass
                
                return True, all_detections, self.detection_method, total_species_count
            else:
                print(f"❌ FFmpeg failed (code {result.returncode})")
                print("Trying fallback codec...")
                cmd_fallback = [
                    'ffmpeg',
                    '-i', temp_avi,
                    '-c:v', 'mpeg4',
                    '-q:v', '5',
                    '-movflags', '+faststart',
                    output_path_final,
                    '-y',
                    '-loglevel', 'error'
                ]
                result2 = subprocess.run(cmd_fallback, capture_output=True, timeout=600)
                
                if result2.returncode == 0 and os.path.exists(output_path_final):
                    print(f"✓ MP4 created with MPEG4 codec")
                    try:
                        os.remove(temp_avi)
                    except:
                        pass
                    return True, all_detections, self.detection_method, total_species_count
                else:
                    return False, [], self.detection_method, {}
                
        else:
            print("❌ AVI file not created")
            return False, [], self.detection_method, {}
