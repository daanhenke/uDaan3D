import pygame, math
import sys


class Camera(object):
    def __init__(self, position=(0, 0, 0), rotation=(0.0, 0), speed=10):
        self.position = list(position)
        self.rotation = list(rotation)
        self.speed = speed

    def event_handler(self, deltatime, key_data):
        speed = deltatime * self.speed

        if key_data[pygame.K_q]:
            self.position[1] += speed
        if key_data[pygame.K_e]:
            self.position[1] -= speed

        x, y = speed * math.sin(self.rotation[1]), speed * math.cos(self.rotation[1])

        if key_data[pygame.K_w]:
            self.position[0] += x
            self.position[2] += y
        if key_data[pygame.K_s]:
            self.position[0] -= x
            self.position[2] -= y

        if key_data[pygame.K_a]:
            self.position[0] -= y
            self.position[2] += x
        if key_data[pygame.K_d]:
            self.position[0] += y
            self.position[2] -= x

        if key_data[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

    def rotate2d(self, position, radians):
        x, y = position

        sin = math.sin(radians)
        cos = math.cos(radians)

        return x * cos - y * sin, y * cos + x * sin

    def handle_rotation(self, event):
        x = float(event.rel[0])
        y = float(event.rel[1])
        x /= 200
        y /= 200

        print(x, y)

        self.rotation[0] += y
        self.rotation[1] += x