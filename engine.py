import pygame
import sys

from camera import Camera
from cube import Cube
from tools import load_obj

pygame.init()
screen = (900, 900)
center_screen = (screen[0] // 2, screen[1] // 2)

display = pygame.display.set_mode(screen)
clock = pygame.time.Clock()
pygame.event.get()
pygame.mouse.get_rel()
pygame.mouse.set_visible(0)
pygame.event.set_grab(1)

radian = 0

camera = Camera(position=(5, -5, 5))

vertices = (0.0, 0.0, 0.0), (0.0, 0.0, 1.0), (0.0, 1.0, 0.0), (0.0, 1.0, 1.0), (1.0, 0.0, 0.0), (1.0, 0.0, 1.0), (1.0, 1.0, 0.0), (1.0, 1.0, 1.0)
faces = (0, 1, 2, 3), (4, 5, 6, 7), (0, 1, 5, 4), (2, 3, 7, 6), (0, 3, 7, 4), (1, 2, 6, 5)
print(faces)

colors = (255, 0, 0), (255, 128, 0), (255, 255, 0), (255, 255, 255), (0, 0, 255), (0, 255, 0)

cubes = [Cube(position=(-1, 0, 0)), Cube(position=(0, 0, 0)), Cube(position=(1, 0, 0)), Cube(position=(3, 0, 0)), Cube(position=(1, 0, 3)), Cube(position=(0, 0, 2)), Cube(position=(-1, 0, 2)), Cube(position=(1, 0, 2)), Cube(position=(2, 0, 2)), Cube(position=(3, 0, 2)), Cube(position=(0, 0, 4)), Cube(position=(-1, 0, 4)), Cube(position=(1, 0, 4)), Cube(position=(2, 0, 4)), Cube(position=(3, 0, 4))]

running = True

while running:
    deltatime = float(clock.tick())/1000

    radian += deltatime

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            camera.handle_rotation(event)

    display.fill((130, 130, 255))

    face_list = []
    face_color = []
    depth = []

    for obj in cubes:

        vertice_list = []
        screen_coords = []

        for x, y, z in obj.vertices:
            x -= camera.position[0]
            y -= camera.position[1]
            z -= camera.position[2]

            x, z = camera.rotate2d((x, z), camera.rotation[1])
            y, z = camera.rotate2d((y, z), camera.rotation[0])

            vertice_list += [(x, y, z)]

            f = 200 / z
            x *= f
            y *= f

            screen_coords += [(center_screen[0] + int(x), center_screen[1] + int(y))]

        for f in range(len(obj.faces)):
            face = obj.faces[f]

            on_screen = False
            for i in face:
                x, y = screen_coords[i]
                if 0 < vertice_list[i][2] < x < screen[0] and 0 < y < screen[1]:
                    on_screen = True
                    break

            if on_screen:
                coords = [screen_coords[i] for i in face]
                face_list += [coords]
                face_color += [obj.colors[f % 6]]

                depth += [sum(sum(vertice_list[j][i] for j in face) ** 2 for i in range(3))]

    order = sorted(range(len(face_list)), key=lambda i: depth[i], reverse=True)

    for i in order:
        try:
            pygame.draw.polygon(display, face_color[i], face_list[i])
        except:
            pass

    pygame.display.flip()

    camera.event_handler(deltatime, pygame.key.get_pressed())

pygame.quit()
sys.exit()