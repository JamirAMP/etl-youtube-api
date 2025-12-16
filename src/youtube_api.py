from googleapiclient.discovery import build
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)

class YouTubeAPI:
    """
    Cliente para interactuar con YouTube Data API v3.
    Proporciona métodos para buscar videos, obtener detalles, comentarios y canales.
    """
    
    def __init__(self, api_key):        
        self.youtube = build('youtube', 'v3', developerKey=api_key, credentials=None)
        
    def search_videos(self, query, max_results=50, published_after=None, published_before=None, order='relevance'):
        try:
            search_request = self.youtube.search().list(
                q=query,
                part='snippet',
                type='video',
                order=order,
                maxResults=min(max_results, 50),
                publishedAfter=published_after,
                publishedBefore=published_before
            )
            search_response = search_request.execute()
            
            video_ids = [item['id']['videoId'] for item in search_response['items']]
            logger.info(f"Encontrados {len(video_ids)} videos para query: '{query}'")
            
            return self.get_video_details(video_ids) 
        except Exception as e:
            logger.error(f"Error searching videos: {e}")
            return []
    
    def get_video_details(self, video_ids):
        videos_data = []
        
        try:
            videos_request = self.youtube.videos().list(
                part='snippet,statistics,contentDetails',
                id=','.join(video_ids)
            )
            videos_response = videos_request.execute()
            
            for video in videos_response['items']:
                video_info = {
                    'video_id': video['id'],
                    'titulo': video['snippet']['title'],
                    'descripcion': video['snippet'].get('description', ''),
                    'canal_id': video['snippet']['channelId'],
                    'canal_nombre': video['snippet']['channelTitle'],
                    'fecha_publicacion': video['snippet']['publishedAt'],
                    'duracion': video['contentDetails']['duration'],
                    'vistas': int(video['statistics'].get('viewCount', 0)),
                    'likes': int(video['statistics'].get('likeCount', 0)),
                    'comentarios': int(video['statistics'].get('commentCount', 0)),
                    'tags': video['snippet'].get('tags', []),
                    'categoria_id': video['snippet'].get('categoryId', ''),
                    'thumbnail_url': video['snippet']['thumbnails']['high']['url'],
                    'fecha_extraccion': datetime.now(timezone.utc).isoformat()
                }
                videos_data.append(video_info)
            
            logger.info(f"Obtenidos detalles para {len(videos_data)} videos")
            return videos_data
        except Exception as e:
            logger.error(f"Error obteniendo detalles de videos: {e}")
            return []
        
    
    def get_comments(self, video_id, max_comments=100):
        comments_data = []
        try:
            comments_request = self.youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                maxResults=min(max_comments, 100),
                textFormat='plainText'
            )
            comments_response = comments_request.execute()
            
            for item in comments_response['items']:
                comment = item['snippet']['topLevelComment']['snippet']
                comment_info = {
                    'video_id': video_id,
                    'comment_id': item['id'],
                    'author': comment['authorDisplayName'],
                    'text': comment['textDisplay'],
                    'like_count': comment.get('likeCount', 0),
                    'published_at': comment['publishedAt'],
                    'updated_at': comment['updatedAt'],
                    'fecha_extraccion': datetime.now(timezone.utc).isoformat()
                }
                comments_data.append(comment_info)
            
            logger.info(f"Obtenidos {len(comments_data)} comentarios para video ID: {video_id}")
            
        except Exception as e:
            logger.warning(f"Error obteniendo comentarios para video ID {video_id}: {e}")
        
        return comments_data
    
    def get_info_channel(self, channel_id):
        try:
            channel_request = self.youtube.channels().list(
                part='snippet,statistics',
                id=channel_id
            )
            channel_response = channel_request.execute()
            
            if not channel_response['items']:
                logger.warning(f"No se encontró información para el canal ID: {channel_id}")
                return None
            
            channel = channel_response['items'][0]
            channel_info = {
                'canal_id': channel['id'],
                'nombre': channel['snippet']['title'],
                'descripcion': channel['snippet'].get('description', ''),
                'fecha_creacion': channel['snippet']['publishedAt'],
                'pais': channel['snippet'].get('country', ''),
                'suscriptores': int(channel['statistics'].get('subscriberCount', 0)),
                'videos_totales': int(channel['statistics'].get('videoCount', 0)),
                'vistas_totales': int(channel['statistics'].get('viewCount', 0)),
                'fecha_extraccion': datetime.now(timezone.utc).isoformat()
            }
            logger.info(f"Obtenida información para el canal: {channel_info['nombre']}")
            return channel_info
        except Exception as e:
            logger.error(f"Error obteniendo información del canal ID {channel_id}: {e}")
        
        return None