class ChannelExtractor:
    def __init__(self, youtube_api):
        self.youtube_api = youtube_api

    def extract(self, videos):
        channel_ids = set(v["canal_id"] for v in videos)
        channels = []
        for cid in channel_ids:
            info = self.youtube_api.get_info_channel(cid)
            if info:
                channels.append(info)
        return channels
