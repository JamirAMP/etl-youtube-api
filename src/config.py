import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    
    YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
    
    DB_HOST = os.getenv("YT_DB_HOST", "youtube-postgres")
    DB_PORT = int(os.getenv("YT_DB_PORT", 5432))
    DB_NAME = os.getenv("YT_DB_NAME", "youtube_analytics")
    DB_USER = os.getenv("YT_DB_USER", "yt_user")
    DB_PASSWORD = os.getenv("YT_DB_PASSWORD", "yt_pass")    
    
    MAX_VIDEOS = int(os.getenv('MAX_VIDEOS', 50))
    MAX_COMENTARIOS = int(os.getenv('MAX_COMENTARIOS', 100))
    EXTRACT_COMMENTS = os.getenv('EXTRACT_COMMENTS', 'True').lower() == 'true'
    
    DATA_DIR = os.getenv('DATA_DIR', '/opt/airflow/data')
    LOG_DIR = os.getenv('LOG_DIR', '/opt/airflow/logs')