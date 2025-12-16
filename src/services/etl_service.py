class YouTubeETLService:
    """
    Servicio de orquestación del proceso ETL de YouTube.
    Coordina la extracción, transformación y carga de videos, comentarios y canales.
    """
    
    def __init__(self, video_extractor, comment_extractor, channel_extractor, loader, cleaner):
        self.video_extractor = video_extractor
        self.comment_extractor = comment_extractor
        self.channel_extractor = channel_extractor
        self.loader = loader
        self.cleaner = cleaner
        
    def run(self, technologies: list[dict], settings: dict, year=None):
        # Extract videos for each technology
        videos = []
        published_after = None
        published_before = None
        
        if year:
            published_after = f"{year}-01-01T00:00:00Z"
            published_before = f"{year}-12-31T23:59:59Z"
            
        for tech in technologies:
            result = self.video_extractor.search_videos(
                query=tech["search_query"],
                max_results=settings["max_videos"],
                published_after=published_after,
                published_before=published_before
            )
            for v in result:
                v["search_query"] = tech["search_query"]
                v["technology_id"] = tech["technology_id"]
            videos.extend(result)
        
        clean_videos = self.cleaner.clean_video_data(videos)
        self.loader.load_data("raw_videos", clean_videos)

        # Extract comments if enabled
        if settings.get("extract_comments", False):
            comments = []
            for video in clean_videos:
                video_comments = self.comment_extractor.get_comments(
                    video["video_id"], 
                    settings["max_comments"]
                )
                comments.extend(video_comments)
            
            clean_comments = self.cleaner.clean_comment_data(comments)
            self.loader.load_data("raw_comments", clean_comments)

        # Extract unique channels
        channel_ids = list(set(v["canal_id"] for v in clean_videos if v.get("canal_id")))
        channels = []
        for channel_id in channel_ids:
            channel_info = self.channel_extractor.get_info_channel(channel_id)
            if channel_info:
                channels.append(channel_info)
        
        clean_channels = self.cleaner.clean_channel_data(channels)
        self.loader.load_data("raw_channels", clean_channels)