from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QLineEdit, QPushButton, QFileDialog, QListWidget, QListWidgetItem,
                               QMessageBox, QSizePolicy, QComboBox, QSpinBox)
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Qt
from utils import format_duration, format_filesize_mb, current_directory


WIDTH, HEIGHT = 500, 600


dark_theme_style = open('themes/dark_theme.qss').read()
light_theme_style = open('themes/light_theme.qss').read()


class YouTubeDownloaderGUI(QWidget):
    def __init__(self, youtube_api):
        super().__init__()
        self.youtube_api = youtube_api
        self.setup_ui()
        self.current_theme = 'light'
        self.apply_theme()

    def setup_ui(self):
        icon_path = "icon.png"
        app_icon = QIcon(icon_path)
        self.setWindowIcon(app_icon)

        self.setWindowTitle("YouTube Downloader")
        self.setFixedSize(WIDTH, HEIGHT)

        self.toggle_theme_button = QPushButton("🌙")
        self.toggle_theme_button.clicked.connect(self.toggle_theme)

        self.search_label = QLabel("Enter Search Query:")
        self.search_input = QLineEdit()

        self.search_button = QPushButton("Search 🔍")
        self.search_button.clicked.connect(self.search_videos)

        max_results_label = QLabel("Max Results:")
        self.max_results_spinbox = QSpinBox()
        self.max_results_spinbox.setRange(5, 50)
        self.max_results_spinbox.setValue(10)

        order_label = QLabel("Order:")
        self.order_combobox = QComboBox()
        self.order_combobox.addItems(["Relevance", "Date", "Rating"])

        duration_label = QLabel("Video Duration:")
        self.duration_combobox = QComboBox()
        self.duration_combobox.addItems(["Any", "Long", "Medium", "Short"])

        self.video_list_label = QLabel("Select Video to Download:")
        self.video_list = QListWidget()
        self.video_list.itemClicked.connect(self.handle_list_item_click)

        self.directory_label = QLabel("Download Directory:")
        self.directory_display = QLineEdit()
        self.directory_display.setText(current_directory())
        self.directory_display.setReadOnly(True)
        self.browse_button = QPushButton("Browse 📂")
        self.browse_button.clicked.connect(self.browse_directory)

        self.title_video_display = QLineEdit()
        self.title_video_display.setReadOnly(True)
        self.stream_selection_label = QLabel("Video:")
        self.stream_selection_combobox = QComboBox()
        self.download_button = QPushButton("Download 💾")
        self.download_button.clicked.connect(self.download_video)
        self.result_label = QLabel("")

        layout = QVBoxLayout()

        settings_layout = QVBoxLayout()
        settings_layout.addWidget(self.toggle_theme_button)
        settings_layout.setAlignment(Qt.AlignTop | Qt.AlignRight)
        layout.addLayout(settings_layout)

        search_layout = QHBoxLayout()
        search_layout.addWidget(self.search_label)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)
        layout.addLayout(search_layout)

        filters_layout = QHBoxLayout()
        filters_layout.addWidget(max_results_label)
        filters_layout.addWidget(self.max_results_spinbox)
        filters_layout.addWidget(order_label)
        filters_layout.addWidget(self.order_combobox)
        filters_layout.addWidget(duration_label)
        filters_layout.addWidget(self.duration_combobox)
        layout.addLayout(filters_layout)

        layout.addWidget(self.video_list_label)
        layout.addWidget(self.video_list)

        directory_layout = QHBoxLayout()
        directory_layout.addWidget(self.directory_label)
        directory_layout.addWidget(self.directory_display)
        directory_layout.addWidget(self.browse_button)
        layout.addLayout(directory_layout)

        download_layout = QHBoxLayout()
        download_layout.addWidget(self.stream_selection_label)
        download_layout.addWidget(self.title_video_display)
        download_layout.addWidget(self.stream_selection_combobox)
        self.stream_selection_combobox.setFixedWidth(100)
        download_layout.addWidget(self.download_button)
        layout.addLayout(download_layout)

        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def apply_theme(self):
        if self.current_theme == 'light':
            self.setStyleSheet(light_theme_style)
            self.toggle_theme_button.setText("🌙")
        else:
            self.setStyleSheet(dark_theme_style)
            self.toggle_theme_button.setText("☀️")
        self.toggle_theme_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.toggle_theme_button.setMinimumSize(self.toggle_theme_button.sizeHint())
        self.toggle_theme_button.setMaximumSize(self.toggle_theme_button.sizeHint())

    def toggle_theme(self):
        if self.current_theme == 'light':
            self.current_theme = 'dark'
        else:
            self.current_theme = 'light'
        self.apply_theme()

    def search_videos(self):
        query = self.search_input.text()
        max_results = self.max_results_spinbox.value()
        order = self.order_combobox.currentText().lower()
        duration = self.duration_combobox.currentText().lower()
        videos = self.youtube_api.search_videos(query, max_results, order, duration)

        self.video_list.clear()

        for video in videos:
            title = video["title"]
            video_id = video["video_id"]
            video_url = video["video_url"]
            thumbnail_url = video["thumbnail_url"]
            author = video["author"]
            duration = video["duration"]
            formatted_duration = format_duration(duration)

            video_widget = QWidget()
            layout = QHBoxLayout(video_widget)
            video_widget.setContentsMargins(0, 0, 0, 0)

            thumbnail_label = QLabel()
            thumbnail = QPixmap()
            thumbnail_data = self.youtube_api.get_thumbnail(thumbnail_url)
            thumbnail.loadFromData(thumbnail_data)
            scaled_thumbnail = thumbnail.scaled(120, 68, Qt.KeepAspectRatio)
            thumbnail_label.setPixmap(scaled_thumbnail)
            thumbnail_label.setAlignment(Qt.AlignLeft)  # Устанавливаем выравнивание влево
            thumbnail_label.setContentsMargins(0, 0, 0, 0)
            thumbnail_label.setFixedSize(120, 68)
            layout.addWidget(thumbnail_label)

            info_layout = QVBoxLayout()
            info_layout.setContentsMargins(0, 0, 0, 0)
            info_layout.setAlignment(Qt.AlignLeft)
            title_label = QLabel(f"{title}", objectName="TitleLabel")
            author_label = QLabel(f"{author}")
            duration_label = QLabel(f"{formatted_duration}")
            info_layout.addWidget(title_label)
            info_layout.addWidget(author_label)
            info_layout.addWidget(duration_label)
            layout.addLayout(info_layout)

            list_item = QListWidgetItem()
            list_item.setSizeHint(video_widget.sizeHint())

            list_item.setData(Qt.UserRole, video_url)

            self.video_list.addItem(list_item)
            self.video_list.setItemWidget(list_item, video_widget)

    def handle_list_item_click(self, item):
        selected_widget = self.video_list.itemWidget(item)
        video_url = item.data(Qt.UserRole)
        streams = self.youtube_api.get_streams(video_url)

        title = selected_widget.findChild(QLabel, "TitleLabel").text()
        self.title_video_display.setText(title)

        self.stream_selection_combobox.clear()

        highest_resolution_stream = max(
            (stream for stream in streams if stream.type == "video" and stream.includes_audio_track),
            key=lambda stream: int(stream.resolution[:-1]) if stream.resolution[:-1].isdigit() else 0
        )

        for stream in streams:
            formatted_size = format_filesize_mb(stream.filesize)
            item_text = f"{stream.resolution} ({formatted_size})"
            self.stream_selection_combobox.addItem(item_text)

            index = self.stream_selection_combobox.findText(item_text)
            self.stream_selection_combobox.setItemData(index, stream)

            if stream == highest_resolution_stream:
                index = self.stream_selection_combobox.findText(item_text)
                self.stream_selection_combobox.setCurrentIndex(index)

    def browse_directory(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(self, "Select Download Directory", options=options)
        if directory:
            self.directory_display.setText(directory)

    def download_video(self):
        selected_item = self.video_list.currentItem()
        if not selected_item:
            return

        selected_widget = self.video_list.itemWidget(selected_item)
        title = selected_widget.findChild(QLabel, "TitleLabel").text()
        download_directory = self.directory_display.text()

        selected_index = self.stream_selection_combobox.currentIndex()
        selected_stream = self.stream_selection_combobox.itemData(selected_index)

        success, error = self.youtube_api.download_video(download_directory, selected_stream)

        if success:
            QMessageBox.information(self, "Download Complete", f"Video '{title}' downloaded successfully.")
        else:
            QMessageBox.warning(self, "Download Error", f"An error occurred while downloading the video:\n{str(error)}")
