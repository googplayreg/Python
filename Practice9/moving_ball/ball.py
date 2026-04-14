import pygame

class Ball:
    def __init__(self, x, y, radius, color, step):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.step = step # На сколько пикселей сдвигаемся за раз

    def draw(self, screen):
        """Рисует шарик на указанном экране."""
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def move(self, direction, screen_width, screen_height):
        """Двигает шарик, если он не выходит за границы."""
        new_x = self.x
        new_y = self.y

        if direction == "UP":
            new_y -= self.step
        elif direction == "DOWN":
            new_y += self.step
        elif direction == "LEFT":
            new_x -= self.step
        elif direction == "RIGHT":
            new_x += self.step

        # Проверка границ (учитываем радиус, чтобы шарик не заходил краем за экран)
        if (self.radius <= new_x <= screen_width - self.radius) and \
           (self.radius <= new_y <= screen_height - self.radius):
            self.x = new_x
            self.y = new_y