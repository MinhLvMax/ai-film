import yt_dlp
import subprocess


class YoutubeDLPClient:
    def __init__(self):
        self.options = {
            "quiet": True,
            "extract_flat": True,
            "skip_download": True,
        }

    def search(self, keyword, limit=5):
        with yt_dlp.YoutubeDL(self.options) as ydl:
            result = ydl.extract_info(
                f"ytsearch{limit}:{keyword}",
                download=False
            )

        return self._view_count_rerank(result["entries"])

    def _view_count_rerank(self, search_result):
        return sorted(
            search_result,
            key=lambda entry: entry.get("view_count") or 0,
            reverse=True,
        )

    def download(self, video_url):




if __name__ == '__main__':
    from pprint import pprint

    # Sử dụng
    youtube = YoutubeDLPClient()
    videos = youtube.search("Suriname", 10)
    for video in videos:
        pprint(video)
        # pprint({
        #     'uploader_url': video.get("uploader_url"),
        #     "channel": video.get("channel"),
        #     "title": video.get("title"),
        #     "description": video.get("description"),
        #     "url": video.get("url"),
        #     "view_count": video.get("view_count"),
        # })
