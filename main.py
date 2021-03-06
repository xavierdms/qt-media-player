import sys
import os
import time
from PySide2.QtUiTools import QUiLoader #allows us to import .ui files
from PySide2.QtWidgets import QApplication, QLineEdit, QPushButton, QFileDialog, QAction, QLabel, QSlider
from PySide2.QtCore import QFile, QObject, QUrl, Qt
from PySide2.QtMultimedia import QMediaPlayer, QMediaPlaylist

class MainWindow(QObject):

    #class constructor
    def __init__(self, ui_file, parent=None):

        #reference to our music player
        self.music_player = QMediaPlayer()

        self.music_playlist = QMediaPlaylist()
        self.music_player.setVolume(80)

        #call parent QObject constructor
        super(MainWindow, self).__init__(parent)

        #load the UI file into Python
        ui_file = QFile(ui_file)
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.window = loader.load(ui_file)

        self.window.setWindowFlags(Qt.MSWindowsFixedSizeDialogHint)
        self.window.setWindowTitle("SynthWAV")
        
        #always remember to close files
        ui_file.close()

        #add event listeners
        open_action = self.window.findChild(QAction, 'action_open')
        open_action.triggered.connect(self.open_action_triggered)

        quit_action = self.window.findChild(QAction, 'action_quit')
        quit_action.triggered.connect(self.quit_action_triggered)

        open_button = self.window.findChild(QPushButton, 'open_button')
        open_button.clicked.connect(self.open_action_triggered)

        quit_button = self.window.findChild(QPushButton, 'quit_button')
        quit_button.clicked.connect(self.quit_action_triggered)

        play_button = self.window.findChild(QPushButton, 'play_button')
        play_button.clicked.connect(self.play_button_clicked)

        pause_button = self.window.findChild(QPushButton, 'pause_button')
        pause_button.clicked.connect(self.pause_button_clicked) 

        stop_button = self.window.findChild(QPushButton, 'stop_button')
        stop_button.clicked.connect(self.stop_button_clicked)
        
        progress_slider = self.window.findChild(QSlider, 'progress_slider')
        self.music_player.positionChanged.connect(self.update_progress)
        progress_slider.sliderMoved.connect(self.scrub_progress)

        volume_slider = self.window.findChild(QSlider, 'volume_slider')
        volume_slider.setValue(self.music_player.volume())
        volume_slider.sliderMoved.connect(self.adjust_volume)

        next_button = self.window.findChild(QPushButton, 'next_button')
        next_button.clicked.connect(self.next_button_clicked)

        previous_button = self.window.findChild(QPushButton, 'previous_button')
        previous_button.clicked.connect(self.previous_button_clicked)

        fforward_button = self.window.findChild(QPushButton, 'fforward_button')
        fforward_button.clicked.connect(self.fforward_button_clicked)

        fbackward_button = self.window.findChild(QPushButton, 'fbackward_button')
        fbackward_button.clicked.connect(self.fbackward_button_clicked)

        self.music_playlist.currentMediaChanged.connect(self.change_title)

        #show window to user
        self.window.show()

    def open_action_triggered(self):
        files = QFileDialog.getOpenFileNames(self.window, "Add songs to playlist")
        for i in range(len(files[0])):
            self.music_playlist.addMedia(QUrl.fromLocalFile(str(files[0][i])))
        self.music_playlist.setCurrentIndex(0)
        self.music_player.setPlaylist(self.music_playlist)
        
    def change_title(self):
        title_label = self.window.findChild(QLabel, 'media_title')
        show_title_path = self.music_playlist.currentMedia().canonicalUrl().fileName()
        show_title = os.path.splitext(show_title_path)
        title_label.setText(show_title[0])
        
    def quit_action_triggered(self):
        self.window.close()

    def play_button_clicked(self):
        self.music_player.play()

    def pause_button_clicked(self):
        self.music_player.pause()

    def stop_button_clicked(self):
        self.music_player.stop()

    def next_button_clicked(self):
        self.music_playlist.next()

    def previous_button_clicked(self):
        self.music_playlist.previous()

    def fforward_button_clicked(self):
        self.music_player.setPosition(self.music_player.position()+10000)

    def fbackward_button_clicked(self):
        self.music_player.setPosition(self.music_player.position()-10000)

    def update_progress(self):
        progress_slider = self.window.findChild(QSlider, 'progress_slider')

        if self.music_player.duration != 0:
            progress_slider.setMaximum(self.music_player.duration())
            total_sec = (self.music_player.duration()/1000)%60
            total_min = (self.music_player.duration()/(1000*60))%60
            if (total_sec < 10):
                total_time = ("%d:0%d" %  (int(total_min), int(total_sec)))
            else:
                total_time = ("%d:%d" %  (int(total_min), int(total_sec)))
            track_duration_label = self.window.findChild(QLabel, 'track_duration_label')
            track_duration_label.setText(total_time)
        
        progress = self.music_player.position()
        progress_slider.setValue(progress)
        cur_sec = (self.music_player.position()/1000)%60
        cur_min = (self.music_player.position()/(1000*60))%60
        if (cur_sec < 10):
            cur_time = ("%d:0%d" %  (int(cur_min), int(cur_sec)))
        else:
            cur_time = ("%d:%d" %  (int(cur_min), int(cur_sec)))
        track_current_label = self.window.findChild(QLabel, 'track_current_label')
        track_current_label.setText(cur_time)

    def scrub_progress(self):
        progress_slider = self.window.findChild(QSlider, 'progress_slider')
        self.music_player.setPosition(progress_slider.sliderPosition())
        cur_min = (self.music_player.position()/1000)%60
        cur_sec = (self.music_player.position()/(1000*60))%60
        if (cur_sec < 10):
            cur_time = ("%d:0%d" %  (int(cur_min), int(cur_sec)))
        else:
            cur_time = ("%d:%d" %  (int(cur_min), int(cur_sec)))
        track_current_label = self.window.findChild(QLabel, 'track_current_label')
        track_current_label.setText(cur_time)

    def adjust_volume(self):
        volume_slider = self.window.findChild(QSlider, 'volume_slider')
        self.music_player.setVolume(volume_slider.sliderPosition())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow('MainWindow.ui')
    sys.exit(app.exec_())
