import shutil
import subprocess
from youtube_transcript_api import YouTubeTranscriptApi


class MediaProcessor:

    def extract_audio(self, video_path, audio_path):
        # Kiểm tra FFmpeg
        if not shutil.which("ffmpeg"):
            print("FFmpeg chưa được cài. Đang cài...")

            subprocess.run([
                "winget",
                "install",
                "Gyan.FFmpeg",
                "--accept-source-agreements",
                "--accept-package-agreements"
            ], check=True)

        result = subprocess.run(
            ["where.exe", "ffmpeg"],
            capture_output=True,
            text=True,
            check=True
        )

        ffmpeg_path = result.stdout.strip()

        subprocess.run([
            ffmpeg_path,
            '-y',
            "-i", video_path,
            "-vn",
            "-acodec", "aac",
            audio_path
        ], check=True)

    def extract_transcription_by_ytta(self, video_search_results: list[dict]):
        '''
        Hàm này rút thêm transcript từ các kết quả video tìm kiếm được, nên rút ngắn số lượng video tìm kiếm được lại để tránh bị chặn ip
        Cách làm này rất hay bị chặn, có lẽ nên dùng cách khác
        :param video_search_results: Các video tìm kiếm được trên youtobe
        :return: video_search_results có thêm key 'transcript'
        '''
        api = YouTubeTranscriptApi()
        for video in video_search_results:
            video_id = video['id']
            transcripts = api.list(video_id)
            transcript = next(iter(transcripts))
            if transcript.language_code != "en" and transcript.is_translatable:
                transcript = transcript.translate("en")
            fetched = transcript.fetch().to_raw_data()
            video.update({
                'transcript': fetched,
            })
        return video_search_results

    def extract_transcription_by_extension(self, video_url: str):
        ...


if __name__ == '__main__':
    from pathlib import Path
    from pprint import pprint
    from src.infrastructure.search_engine.youtobe_dlp_search import YoutubeDLPClient

    media_processor = MediaProcessor()
    video_path = Path(r'C:\Users\Admin\Downloads\videoplayback.mp4')
    # audio_path = video_path.parent / f'{video_path.stem}.m4a'
    # media_processor.extract_audio(video_path, audio_path)

    youtube_client = YoutubeDLPClient()
    search_results = youtube_client.search('SURINAME', limit=1)

    transcription_result = media_processor.extract_transcription_by_ytta(search_results)
    pprint(transcription_result)
