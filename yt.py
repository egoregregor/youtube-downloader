from googleapiclient.discovery import build
from pytube import YouTube
import aiohttp
import asyncio


class YouTubeAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.youtube = build("youtube", "v3", developerKey=self.api_key)
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def search_videos(self, query, max_results, order, duration):
        if not query:
            return

        search_response = self.youtube.search().list(
            q=query,
            part="id,snippet",
            type="video",
            maxResults=max_results,
            order=order,
            videoDuration=duration
        ).execute()

        videos = list()

        for item in search_response["items"]:
            title = item["snippet"]["title"]
            video_id = item["id"]["videoId"]
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            thumbnail_url = item["snippet"]["thumbnails"]["default"]["url"]
            author = item["snippet"]["channelTitle"]

            video_info = self.youtube.videos().list(
                part="snippet,contentDetails",
                id=video_id
            ).execute()
            duration = video_info["items"][0]["contentDetails"]["duration"]

            video = {"title": title,
                     "video_id": video_id,
                     "video_url": video_url,
                     "thumbnail_url": thumbnail_url,
                     "author": author,
                     "duration": duration}
            videos.append(video)

        return videos

    def get_streams(self, video_url):
        yt = YouTube(video_url)

        streams = list()

        for stream in yt.streams:
            if stream.type == "video" and stream.includes_audio_track:
                streams.append(stream)

        return streams

    def download_video(self, download_directory, stream):
        try:
            stream.download(download_directory)
            return True, 0
        except Exception as e:
            return False, e

    async def get_thumbnail_async(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.read()

    def get_thumbnail(self, url):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self.get_thumbnail_async(url))
