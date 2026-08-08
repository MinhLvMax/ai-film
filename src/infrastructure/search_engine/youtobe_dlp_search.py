import yt_dlp
from src.infrastructure.helper import run_cli
from src.infrastructure.python_logger import PythonLogger


class YoutubeDLPClient:
    def __init__(self, logger=None):
        self.options = {
            "quiet": True,
            "extract_flat": True,
            "skip_download": True,
        }
        self.logger = logger or PythonLogger(name=__name__)

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

    def download(self, video_url, output):
        run_cli(
            'yt-dlp',
            video_url,
            '-P',
            str(output)
        )
        self.logger.info("Video downloaded")


if __name__ == '__main__':
    from pprint import pprint
    from src.config import Config

    # Sử dụng
    youtube = YoutubeDLPClient()

    # Test search
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

    # Test download
    # youtube.download('https://youtu.be/IjO79uKMkcw?si=3k8-Y2J41dYvVPAW', Config.DOWNLOADS)
