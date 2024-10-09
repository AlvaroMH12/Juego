import pygame 
import sys

pygame.init()

tamaño=(800, 500)

#ventana 
 
screen= pygame.display.set_mode(tamaño)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
