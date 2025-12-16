class VideoExtractor:
    
    def __init__(self, youtube_api):
        self.youtube_api = youtube_api

    def extract(self, queries, max_videos, published_after=None, published_before=None):
        videos = []
        for q in queries:
            result = self.youtube_api.search_videos(q, max_videos,published_after, published_before)
            for v in result:
                v["technology"] = q
            videos.extend(result)
        return videos
