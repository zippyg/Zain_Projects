import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QComboBox, QProgressBar, QMessageBox, QSizePolicy, QGridLayout
from PyQt5.QtCore import Qt, QThread, pyqtSignal

# Add the parent directory to the system path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from spotify_api import get_spotify_client, get_liked_songs, get_playlist_songs
from youtube_api import search_youtube
from downloader import download_song
from config.config import YOUTUBE_API_KEYS

class DownloadThread(QThread):
    update_progress = pyqtSignal(str, int)
    download_complete = pyqtSignal()
    download_error = pyqtSignal(str)

    def __init__(self, songs, download_path):
        super().__init__()
        self.songs = songs
        self.download_path = download_path
        self._is_paused = False
        self._is_cancelled = False

    def run(self):
        for idx, (song, artist, cover_art_url) in enumerate(self.songs):
            if self._is_cancelled:
                self.update_progress.emit("Download cancelled", len(self.songs))
                break

            while self._is_paused:
                self.msleep(500)

            self.update_progress.emit(f"Searching for {song} by {artist}", idx)
            video_id = search_youtube(song, artist)
            if video_id:
                self.update_progress.emit(f"Downloading {song}", idx)
                success = download_song(video_id, song, artist, cover_art_url, output_dir=self.download_path)
                if not success:
                    self.download_error.emit(f"Failed to download {song} by {artist}")
            else:
                self.update_progress.emit(f"Could not find {song} by {artist} on YouTube", idx)
        self.download_complete.emit()

    def pause(self):
        self._is_paused = True

    def resume(self):
        self._is_paused = False

    def cancel(self):
        self._is_cancelled = True

class SpotifyYouTubeDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Spotify YouTube Downloader")
        self.setGeometry(100, 100, 600, 500)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.instruction_label = QLabel(
            "Welcome to Spotify YouTube Downloader!\n\n"
            "How to use this app:\n"
            "1. Enter your Spotify Client ID, Client Secret, and Redirect URI. "
            "You can obtain these from the Spotify Developer Dashboard.\n"
            "2. Choose the download path where you want to save your music.\n"
            "3. Click 'Fetch Playlists' to load your playlists from Spotify.\n"
            "4. Select the playlist you want to download from the dropdown menu.\n"
            "5. Click 'Download' to start downloading your selected playlist.\n\n"
        )
        self.instruction_label.setWordWrap(True)
        self.instruction_label.setStyleSheet("padding: 10px; margin-top: 20px;")
        self.instruction_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        layout.addWidget(self.instruction_label)

        # Initialize QLineEdit objects
        self.client_id_entry = QLineEdit()
        self.client_secret_entry = QLineEdit()
        self.redirect_uri_entry = QLineEdit()
        self.download_path_entry = QLineEdit()

        # Create a grid layout for input fields
        grid_layout = QGridLayout()
        row = 0
        grid_layout.addWidget(QLabel("Spotify Client ID:"), row, 0)
        grid_layout.addWidget(self.client_id_entry, row, 1)
        row += 1
        grid_layout.addWidget(QLabel("Spotify Client Secret:"), row, 0)
        grid_layout.addWidget(self.client_secret_entry, row, 1)
        row += 1
        grid_layout.addWidget(QLabel("Spotify Redirect URI:"), row, 0)
        grid_layout.addWidget(self.redirect_uri_entry, row, 1)
        row += 1
        grid_layout.addWidget(QLabel("Download Path:"), row, 0)
        download_path_layout = QHBoxLayout()
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_directory)
        download_path_layout.addWidget(self.download_path_entry)
        download_path_layout.addWidget(self.browse_button)
        grid_layout.addLayout(download_path_layout, row, 1)
        layout.addLayout(grid_layout)

        self.fetch_playlists_button = QPushButton("Fetch Playlists")
        self.fetch_playlists_button.clicked.connect(self.fetch_playlists)
        layout.addWidget(self.fetch_playlists_button)

        self.playlist_combobox = QComboBox()
        layout.addWidget(self.playlist_combobox)

        self.download_button = QPushButton("Download")
        self.download_button.clicked.connect(self.start_download)
        layout.addWidget(self.download_button)

        self.pause_button = QPushButton("Pause")
        self.pause_button.clicked.connect(self.pause_download)
        self.pause_button.setEnabled(False)
        layout.addWidget(self.pause_button)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.cancel_download)
        self.cancel_button.setEnabled(False)
        layout.addWidget(self.cancel_button)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        self.progress_label = QLabel("")
        layout.addWidget(self.progress_label)

        # Add signature label at the bottom
        self.signature_label = QLabel("© 2024 Zain Mughal - All Rights Reserved")
        self.signature_label.setAlignment(Qt.AlignCenter)  # Center-align the text
        self.signature_label.setStyleSheet("font-size: 10px; color: gray;")
        layout.addWidget(self.signature_label)

        self.setLayout(layout)


    def browse_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.download_path_entry.setText(directory)

    def fetch_playlists(self):
        client_id = self.client_id_entry.text()
        client_secret = self.client_secret_entry.text()
        redirect_uri = self.redirect_uri_entry.text()

        if not all([client_id, client_secret, redirect_uri]):
            QMessageBox.critical(self, "Error", "Please fill in all fields")
            return

        self.progress_label.setText("Initializing Spotify client...")
        self.sp = get_spotify_client(client_id, client_secret, redirect_uri)
        self.progress_label.setText("Fetching playlists...")

        playlists = self.sp.current_user_playlists()
        playlist_options = ["Liked Songs"] + [playlist['name'] for playlist in playlists['items']]
        self.playlist_combobox.clear()
        self.playlist_combobox.addItems(playlist_options)

        self.progress_label.setText("Playlists fetched. Select one from the dropdown.")

    def start_download(self):
        download_path = self.download_path_entry.text()
        selected_playlist = self.playlist_combobox.currentText()

        if not all([download_path, selected_playlist]):
            QMessageBox.critical(self, "Error", "Please fill in all fields and select a playlist")
            return

        if selected_playlist == "Liked Songs":
            playlist_songs = get_liked_songs(self.sp)
        else:
            playlists = self.sp.current_user_playlists()
            playlist_idx = [playlist['name'] for playlist in playlists['items']].index(selected_playlist) 
            playlist_id = playlists['items'][playlist_idx]['id']
            playlist_songs = get_playlist_songs(self.sp, playlist_id)

        self.progress_bar.setMaximum(len(playlist_songs))
        self.download_thread = DownloadThread(playlist_songs, download_path)
        self.download_thread.update_progress.connect(self.update_progress)
        self.download_thread.download_complete.connect(self.download_complete)
        self.download_thread.download_error.connect(self.download_error)
        self.download_thread.start()

        self.pause_button.setEnabled(True)
        self.cancel_button.setEnabled(True)

    def update_progress(self, message, value):
        self.progress_label.setText(message)
        self.progress_bar.setValue(value)

    def download_complete(self):
        self.progress_label.setText("Download completed!")
        self.progress_bar.setValue(self.progress_bar.maximum())
        self.pause_button.setEnabled(False)
        self.cancel_button.setEnabled(False)

    def download_error(self, message):
        QMessageBox.warning(self, "Download Error", message)
        self.pause_button.setEnabled(False)
        self.cancel_button.setEnabled(False)

    def pause_download(self):
        self.download_thread.pause()
        self.pause_button.setText("Resume")
        self.pause_button.clicked.disconnect()
        self.pause_button.clicked.connect(self.resume_download)

    def resume_download(self):
        self.download_thread.resume()
        self.pause_button.setText("Pause")
        self.pause_button.clicked.disconnect()
        self.pause_button.clicked.connect(self.pause_download)

    def cancel_download(self):
        self.download_thread.cancel()
        self.progress_label.setText("Download cancelled")
        self.pause_button.setEnabled(False)
        self.cancel_button.setEnabled(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Apply dark theme stylesheet
    app.setStyleSheet("""
        QWidget {
            background-color: #2b2b2b;
            color: #ffffff;
            font-family: Arial;
        }
        QLabel {
            background-color: transparent;
            color: #ffffff;
        }
        QLineEdit {
            background-color: #3c3c3c;
            color: #ffffff;
            border: 1px solid #555555;
            border-radius: 4px;
            padding: 5px;
        }
        QPushButton {
            background-color: #3c3c3c;
            color: #ffffff;
            border: 1px solid #555555;
            border-radius: 4px;
            padding: 5px;
        }
        QPushButton:hover {
            background-color: #555555;
        }
        QComboBox {
            background-color: #3c3c3c;
            color: #ffffff;
            border: 1px solid #555555;
            border-radius: 4px;
            padding: 5px;
        }
        QComboBox QAbstractItemView {
            background-color: #3c3c3c;
            color: #ffffff;
            border: 1px solid #555555;
        }
        QProgressBar {
            text-align: center;
        }
        QProgressBar::chunk {
            background-color: #55aaff;
        }
    """)
    window = SpotifyYouTubeDownloader()
    window.show()
    sys.exit(app.exec_())
