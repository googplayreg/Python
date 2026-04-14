import pygame
import datetime

class Clock:
    def __init__(self, screen_width, screen_height):
        # Сохраняем центр экрана, чтобы привязать к нему часы
        # self.center = (screen_width // 2, screen_height // 2)
        self.center = (343, 380)

        # Загружаем картинки стрелок
        self.min_hand_orig = pygame.image.load('mickeys_clock/images/minute_hand.png').convert()
        self.sec_hand_orig = pygame.image.load('mickeys_clock/images/second_hand.png').convert()
        
        # Делаем фон стрелок прозрачным
        self.min_hand_orig.set_colorkey((255, 255, 255)) 
        self.sec_hand_orig.set_colorkey((255, 255, 255))

        # Переменные для текущих углов
        self.minute_angle = 0
        self.second_angle = 0

    def update(self):
        # 1. Получаем текущее время системы
        now = datetime.datetime.now()
        seconds = now.second
        minutes = now.minute

        # 2. Переводим время в градусы
        # В круге 360 градусов и 60 делений (минут/секунд). 
        # Значит, 1 секунда = 360 / 60 = 6 градусов.
        # В Pygame вращение идет против часовой стрелки, поэтому ставим "минус".
        self.second_angle = -seconds * 6
        self.minute_angle = -minutes * 6

    def draw(self, screen):
        # Отрисовываем сначала минутную, потом секундную (чтобы она была сверху)
        self._draw_rotated_hand(screen, self.min_hand_orig, self.minute_angle)
        self._draw_rotated_hand(screen, self.sec_hand_orig, self.second_angle)

    def _draw_rotated_hand(self, surface, image, angle):
        # Принцип вращения вокруг центра:
        # 1. Создаем новую повернутую картинку
        rotated_image = pygame.transform.rotate(image, angle)
        
        # 2. Берем прямоугольник новой картинки
        new_rect = rotated_image.get_rect()
        
        # 3. Важнейший момент: приравниваем центр нового (повернутого) 
        # прямоугольника к центру экрана. Так стрелка не будет "улетать".
        new_rect.center = self.center
        
        # 4. Рисуем
        surface.blit(rotated_image, new_rect.topleft)