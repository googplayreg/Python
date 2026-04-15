import pygame
import os

class MusicPlayer:
    def __init__(self, music_folder):
        pygame.mixer.init()
        
        # Находим путь к папке, где лежит сам player.py
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Соединяем путь к скрипту с названием папки music
        self.music_folder = os.path.join(current_dir, music_folder)
        
        self.playlist = []
        self.current_track_index = 0
        self.is_playing = False
        self.is_paused = False
        self.volume = 0.5  # Громкость по умолчанию (50%)
        pygame.mixer.music.set_volume(self.volume)
        
        self.load_playlist()

    def load_playlist(self):
        """Сканирует папку и добавляет все mp3 и wav файлы в список."""
        for file in os.listdir(self.music_folder):
            if file.endswith((".mp3", ".wav")):
                self.playlist.append(os.path.join(self.music_folder, file))
        
        if not self.playlist:
            print("В папке music нет подходящих файлов!")

    def play(self):
        """Запускает текущий трек."""
        if self.playlist:
            pygame.mixer.music.load(self.playlist[self.current_track_index])
            pygame.mixer.music.play()
            self.is_playing = True

    def toggle_pause(self):
        """Ставит на паузу."""
        if self.is_playing:
            if self.is_paused:
                pygame.mixer.music.unpause()
                self.is_paused = False
            else:
                pygame.mixer.music.pause()
                self.is_paused = True

    def stop(self):
        """Останавливает воспроизведение."""
        pygame.mixer.music.stop()
        self.is_playing = False
        self.is_paused = False

    def next_track(self):
        """Переключает на следующий трек (циклично)."""
        if self.playlist:
            self.current_track_index = (self.current_track_index + 1) % len(self.playlist)
            self.play()

    def previous_track(self):
        """Переключает на предыдущий трек (циклично)."""
        if self.playlist:
            self.current_track_index = (self.current_track_index - 1) % len(self.playlist)
            self.play()

    def change_volume(self, delta):
        """Изменяет громкость на delta (например, 0.05 или -0.05)."""
        self.volume += delta
        # Ограничиваем громкость в пределах от 0.0 до 1.0
        if self.volume < 0:
            self.volume = 0
        elif self.volume > 1:
            self.volume = 1
    
        pygame.mixer.music.set_volume(self.volume)

    def get_current_track_name(self):
        """Возвращает только название файла для отображения в UI."""
        if self.playlist:
            return os.path.basename(self.playlist[self.current_track_index])
        return "Нет треков"