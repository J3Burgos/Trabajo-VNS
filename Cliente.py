import pygame
import socket
import sys

width, height = 700, 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Cliente")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("172.20.116.2", 5555))

clock = pygame.time.Clock()

def redraw_window(win, player):
    win.fill((255, 255, 255))
    pygame.draw.rect(win, (0, 255, 0), (player[0], player[1], 50, 50))
    pygame.display.update()

def main():
    run = True
    while run:
        clock.tick(60)  # Limita a 60 frames por segundo
        try:
            data = client.recv(2048).decode()
            player = eval(data)
        except Exception as e:
            print(f"Error al recibir datos: {e}")
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player[0] -= 1
        if keys[pygame.K_RIGHT]:
            player[0] += 1
        if keys[pygame.K_UP]:
            player[1] -= 1
        if keys[pygame.K_DOWN]:
            player[1] += 1
        
        client.send(str.encode(str(player)))
        redraw_window(win, player)

    pygame.quit()
    sys.exit()

main()
