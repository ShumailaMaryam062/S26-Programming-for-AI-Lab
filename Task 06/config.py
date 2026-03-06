import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-12345'
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 500 * 1024 * 1024
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov'}
    
    YOLO_WEIGHTS = 'models/yolov3.weights'
    YOLO_CONFIG = 'models/yolov3.cfg'
    YOLO_NAMES = 'models/coco.names'
    
    CONFIDENCE_THRESHOLD = 0.5
    NMS_THRESHOLD = 0.4
    
    DEFAULT_LATITUDE = 40.7128
    DEFAULT_LONGITUDE = -74.0060
    
    MAP_ZOOM_LEVEL = 12
    DETECTION_RADIUS = 500

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    UPLOAD_FOLDER = 'test_uploads'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
