from datetime import datetime, timezone
from typing import List, Dict

class CleanData:
    """
    Transformador de datos para limpieza y validación.
    Limpia y normaliza datos de videos, comentarios y canales.
    """
    
    @staticmethod
    def clean_channel_data(channels_data: List[Dict]) -> List[Dict]:
        clean_data = []
        seen = set()

        for channel in channels_data:
            canal_id = channel.get("canal_id")
            if not canal_id or canal_id in seen:
                continue

            seen.add(canal_id)

            clean_data.append({
                "canal_id": canal_id,
                "nombre": (channel.get("nombre") or "Unknown").strip(),
                "descripcion": channel.get("descripcion") or "No Description",
                "suscriptores": channel.get("suscriptores") or 0,
                "total_videos": channel.get("videos_totales") or 0,
                "vistas_totales": channel.get("vistas_totales") or 0,
                "pais": channel.get("pais") or "Unknown",
                "fecha_creacion": channel.get("fecha_creacion"),
                "fecha_extraccion": channel.get("fecha_extraccion") or datetime.now(timezone.utc).isoformat()
            })

        return clean_data
    
    @staticmethod
    def clean_video_data(videos_data: List[Dict]) -> List[Dict]:
        clean_data = []
        seen = set()

        for video in videos_data:
            video_id = video.get("video_id")
            if not video_id or video_id in seen:
                continue

            seen.add(video_id)

            clean_data.append({
                "video_id": video_id,
                "titulo": (video.get("titulo") or "No Title").strip(),
                "descripcion": video.get("descripcion") or "No Description",
                "canal_id": video.get("canal_id"),
                "canal_nombre": video.get("canal_nombre"),
                "fecha_publicacion": video.get("fecha_publicacion"),
                "duracion": video.get("duracion") or "N/A",
                "vistas": video.get("vistas") or 0,
                "likes": video.get("likes") or 0,
                "comentarios": video.get("comentarios") or 0,
                "tags": video.get("tags") or [],
                "categoria_id": video.get("categoria_id") or "Uncategorized",
                "thumbnail_url": video.get("thumbnail_url"),
                "technology_id": video.get("technology_id"),
                "search_query": video.get("search_query"),
                "fecha_extraccion": video.get("fecha_extraccion") or datetime.now(timezone.utc).isoformat()
            })

        return clean_data
    
    @staticmethod    
    def clean_comment_data(comments_data: List[Dict]) -> List[Dict]:
        clean_data = []
        seen = set()

        for comment in comments_data:
            comment_id = comment.get("comment_id")
            if not comment_id or comment_id in seen:
                continue

            seen.add(comment_id)

            clean_data.append({
                "comment_id": comment_id,
                "video_id": comment.get("video_id"),
                "author": comment.get("author") or "Anonymous",
                "text": comment.get("text") or "No Comment",
                "likes": comment.get("like_count") or 0,
                "published_at": comment.get("published_at"),
                "fecha_extraccion": comment.get("fecha_extraccion") or datetime.now(timezone.utc).isoformat()
            })

        return clean_data