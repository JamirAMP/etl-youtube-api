import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    
    YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
    
    PROJECT_ID = os.getenv('PROJECT_ID')
    DATASET_ID = os.getenv('DATASET_ID', 'youtube_data')
    CREDENTIALS_PATH = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    
    MAX_VIDEOS = int(os.getenv('MAX_VIDEOS', 50))
    MAX_COMMENTARIOS = int(os.getenv('MAX_COMMENTS', 100))
    EXTRACT_COMMENTS = os.getenv('EXTRACT_COMMENTS', 'True').lower() == 'true'
    
    DATA_DIR = os.getenv('DATA_DIR', '/opt/airflow/data')
    LOG_DIR = os.getenv('LOG_DIR', '/opt/airflow/logs')