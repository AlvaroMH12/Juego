import pygame
import sys

# Inicializar Pygame
pygame.init()

# Configurar el tamaño de la ventana
tamaño = (800, 500)
screen = pygame.display.set_mode(tamaño)

# Cargar la imagen de fondo
fondo = pygame.image.load(r"C:\Users\LENOVO\Documents\Downloads\fondo.png")
fondo = pygame.transform.scale(fondo, tamaño)

# Cargar la imagen de la plataforma
plataforma = pygame.image.load(r"C:\Users\LENOVO\Documents\Downloads\plataforma.png")
plataforma = pygame.transform.scale(plataforma, (150, 20))

# Cargar la imagen de la bolsa de basura
bolsa = pygame.Surface((30, 40))  # Simulando la bolsa de basura como un rectángulo
bolsa.fill((0, 255, 0))  # Color verde

# Definir posiciones de las plataformas
plataformas = [
    (100, 400), (200, 450), (300, 400), (400, 350), (500, 300),
    (600, 450), (700, 375), (800, 500), (900, 400), (1000, 450),
    (1100, 300), (1200, 375), (1300, 425), (1400, 250), (1500, 500),
    (1600, 350), (1700, 450), (1800, 300), (1900, 475), (2000, 400),
    (2100, 500), (2200, 375), (2300, 450), (2400, 350), (2500, 450)
]

# Definir la posición de la bolsa de basura
bolsa_pos = [250 + 60, 350 - 40]

# Definir las posiciones iniciales de los personajes
personaje1_pos = [100, 250]
personaje2_pos = [150, 250]

# Definir el tamaño de los personajes
personaje_size = 50

# Variables para el movimiento
velocidad = 5
gravedad = 0.5
salto_fuerza = 11
personaje1_vel_y = 0
personaje2_vel_y = 0
en_suelo1 = True
en_suelo2 = True

# Variables para recoger la bolsa
tiene_bolsa = False

# Definir la posición del contenedor de basura
contenedor_pos = [4000, 300]  # Contenedor sobre la última plataforma

# Función para calcular el ancho de la plataforma
def calcular_ancho_plataforma(x):
    if x < 300:
        return 150
    elif x < 600:
        return 200
    else:
        return 250

# Función para mostrar la pantalla de bienvenida
def mostrar_bienvenida():
    screen.blit(fondo, (0, 0))  # Dibujar el fondo
    fuente = pygame.font.SysFont('Arial', 48)
    texto_bienvenida = fuente.render("Welcome a Play with Clear", True, (255, 255, 255))
    texto_jugar = fuente.render("Play", True, (255, 255, 0))

    rect_bienvenida = texto_bienvenida.get_rect(center=(tamaño[0] // 2, tamaño[1] // 2 - 30))
    rect_jugar = texto_jugar.get_rect(center=(tamaño[0] // 2, tamaño[1] // 2 + 30))

    pygame.draw.rect(screen, (50, 50, 50), rect_bienvenida.inflate(20, 20))
    pygame.draw.rect(screen, (50, 50, 50), rect_jugar.inflate(20, 20))
    
    screen.blit(texto_bienvenida, rect_bienvenida)
    screen.blit(texto_jugar, rect_jugar)

    pygame.display.flip()
    pygame.time.wait(2000)

# Función para mostrar mensajes de fin de juego
def mostrar_mensaje_final(mensaje, reiniciar=False):
    screen.blit(fondo, (0, 0))
    fuente = pygame.font.SysFont('Arial', 48)
    texto_final = fuente.render(mensaje, True, (255, 255, 255))
    
    rect_final = texto_final.get_rect(center=(tamaño[0] // 2, tamaño[1] // 2 - 30))
    pygame.draw.rect(screen, (50, 50, 50), rect_final.inflate(20, 20))
    screen.blit(texto_final, rect_final)

    if reiniciar:
        texto_jugar_nuevamente = fuente.render("Play Again", True, (255, 255, 0))
        rect_jugar_nuevamente = texto_jugar_nuevamente.get_rect(center=(tamaño[0] // 2, tamaño[1] // 2 + 30 + 30))
        pygame.draw.rect(screen, (50, 50, 50), rect_jugar_nuevamente.inflate(20, 20))
        screen.blit(texto_jugar_nuevamente, rect_jugar_nuevamente)

    pygame.display.flip()
    
    esperando = True
    while esperando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                esperando = False

# Función para reiniciar el juego
def reiniciar_juego():
    global personaje1_pos, personaje2_pos, tiene_bolsa, en_suelo1, en_suelo2, personaje1_vel_y, personaje2_vel_y
    personaje1_pos = [100, 250]
    personaje2_pos = [150, 250]
    tiene_bolsa = False
    en_suelo1 = True
    en_suelo2 = True
    bolsa_pos[0] = 250 + 60
    bolsa_pos[1] = 350 - 40

# Llamar a la función de bienvenida
mostrar_bienvenida()

# Bucle principal del juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    # Movimiento del personaje 1
    if keys[pygame.K_a]:
        personaje1_pos[0] -= velocidad
    if keys[pygame.K_d]:
        personaje1_pos[0] += velocidad
    if keys[pygame.K_w] and en_suelo1:
        personaje1_vel_y = -salto_fuerza
        en_suelo1 = False

    # Movimiento del personaje 2
    if keys[pygame.K_LEFT]:
        personaje2_pos[0] -= velocidad
    if keys[pygame.K_RIGHT]:
        personaje2_pos[0] += velocidad
    if keys[pygame.K_UP] and en_suelo2:
        personaje2_vel_y = -salto_fuerza
        en_suelo2 = False

    # Aplicar gravedad
    personaje1_vel_y += gravedad
    personaje2_vel_y += gravedad

    # Actualizar la posición vertical
    personaje1_pos[1] += personaje1_vel_y
    personaje2_pos[1] += personaje2_vel_y

    # Comprobar colisiones con plataformas
    for plat in plataformas:
        plat_x, plat_y = plat
        plat_ancho = calcular_ancho_plataforma(plat_x)

        # Comprobar si el personaje 1 colisiona con la plataforma
        if (personaje1_pos[0] < plat_x + plat_ancho and
            personaje1_pos[0] + personaje_size > plat_x and
            personaje1_pos[1] + personaje_size > plat_y and
            personaje1_pos[1] + personaje_size <= plat_y + 20):
            personaje1_pos[1] = plat_y - personaje_size
            personaje1_vel_y = 0
            en_suelo1 = True

        # Comprobar si el personaje 2 colisiona con la plataforma
        if (personaje2_pos[0] < plat_x + plat_ancho and
            personaje2_pos[0] + personaje_size > plat_x and
            personaje2_pos[1] + personaje_size > plat_y and
            personaje2_pos[1] + personaje_size <= plat_y + 20):
            personaje2_pos[1] = plat_y - personaje_size
            personaje2_vel_y = 0
            en_suelo2 = True

    # Si los personajes no están en el suelo, permitir la caída
    if not en_suelo1:
        personaje1_pos[1] += gravedad

    if not en_suelo2:
        personaje2_pos[1] += gravedad

    # Comprobar si los personajes han caído por debajo del mapa
    if personaje1_pos[1] > 500 or personaje2_pos[1] > 500:
        mostrar_mensaje_final("¡I'm Sorry, Loser!", reiniciar=True)
        reiniciar_juego()
        continue  # Reiniciar el bucle

    # Comprobar si recogen la bolsa de basura
    if (not tiene_bolsa and
        (personaje1_pos[0] < bolsa_pos[0] + 30 < personaje1_pos[0] + personaje_size and
         personaje1_pos[1] < bolsa_pos[1] + 40 < personaje1_pos[1] + personaje_size and
         en_suelo1) or
        (personaje2_pos[0] < bolsa_pos[0] + 30 < personaje2_pos[0] + personaje_size and
         personaje2_pos[1] < bolsa_pos[1] + 40 < personaje2_pos[1] + personaje_size and
         en_suelo2)):
        tiene_bolsa = True
        bolsa_pos = [-100, -100]  # Mover la bolsa fuera de la vista

    # Comprobar si ambos personajes llevan la bolsa al contenedor
    if tiene_bolsa:
        # Actualizar posición de la bolsa para que siga a los personajes
        bolsa_pos = [(personaje1_pos[0] + personaje2_pos[0]) / 2 - 15,
                     (personaje1_pos[1] + personaje2_pos[1]) / 2 - 20]

        if (personaje1_pos[0] + personaje_size > contenedor_pos[0] and
            personaje1_pos[0] < contenedor_pos[0] + 50 and
            personaje1_pos[1] + personaje_size > contenedor_pos[1] and
            personaje1_pos[1] < contenedor_pos[1] + 50) and \
           (personaje2_pos[0] + personaje_size > contenedor_pos[0] and
            personaje2_pos[0] < contenedor_pos[0] + 50 and
            personaje2_pos[1] + personaje_size > contenedor_pos[1] and
            personaje2_pos[1] < contenedor_pos[1] + 50):
            mostrar_mensaje_final("¡Bien hecho! Sigue aportando al planeta")
            pygame.quit()
            sys.exit()

    # Calcular el centro de los personajes para el desplazamiento de la cámara
    centro_camera_x = (personaje1_pos[0] + personaje2_pos[0]) / 2
    desplazamiento_x = centro_camera_x - tamaño[0] / 2

    # Dibujar el fondo estático
    screen.blit(fondo, (0, 0))

    # Dibujar cada plataforma con el desplazamiento
    for posicion in plataformas:
        plat_x, plat_y = posicion
        plat_ancho = calcular_ancho_plataforma(plat_x)
        screen.blit(plataforma, (plat_x - desplazamiento_x, plat_y))

    # Dibujar la bolsa de basura si ha sido recogida
    if tiene_bolsa:
        screen.blit(bolsa, (bolsa_pos[0] - desplazamiento_x, bolsa_pos[1]))

    # Dibujar el contenedor de basura con el desplazamiento
    pygame.draw.rect(screen, (255, 165, 0), (contenedor_pos[0] - desplazamiento_x, contenedor_pos[1], 50, 50))

    # Dibujar los personajes con el desplazamiento
    pygame.draw.rect(screen, (255, 0, 0), (personaje1_pos[0] - desplazamiento_x, personaje1_pos[1], personaje_size, personaje_size))  # Personaje 1 (rojo)
    pygame.draw.rect(screen, (0, 0, 255), (personaje2_pos[0] - desplazamiento_x, personaje2_pos[1], personaje_size, personaje_size))  # Personaje 2 (azul)

    # Actualizar la pantalla
    pygame.display.flip()