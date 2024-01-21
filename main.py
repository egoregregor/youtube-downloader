import sys
from PySide6.QtWidgets import QApplication
from yt import YouTubeAPI
from gui import YouTubeDownloaderGUI


YOUTUBE_API_KEY = "4IzaSyDxLzj02okeK6U4ZPkCveWafhnqO3qbIk0"


if __name__ == "__main__":
    app = QApplication(sys.argv)

    youtube_api = YouTubeAPI(YOUTUBE_API_KEY)
    window = YouTubeDownloaderGUI(youtube_api)
    window.show()

    app.exec()
