class CommentExtractor:
    def __init__(self, youtube_api, max_videos):
        self.youtube_api = youtube_api
        self.max_videos = max_videos

    def extract(self, videos, max_comments):
        comments = []
        for video in videos[:self.max_videos]:
            comments.extend(
                self.youtube_api.get_comments(
                    video["video_id"], max_comments
                )
            )
        return comments
