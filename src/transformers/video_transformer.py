class VideoTransformer:
    @staticmethod
    def clean(videos: list[dict]) -> list[dict]:
        unique = {}
        for v in videos:
            if v["video_id"] not in unique:
                unique[v["video_id"]] = v
        return list(unique.values())
