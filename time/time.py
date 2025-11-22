import pygame
import datetime
running = True
# Initialize audio
pygame.mixer.init()
# Initialize pygame
pygame.init()
font_path = 'NotoSansDisplay-SemiBold.ttf'
font = pygame.font.Font(font_path, 375)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
pygame.display.set_caption("time")
# Get the current date and time
R,G,B = 0,0,0

while running:
    if R < 255:
        R += 3
    else:
        R = 0   
    if G < 255:
        G += 2
    else:
        G = 0
    if B < 255:
        B += 1
    else:
        B = 0
    R = min(R, 255)
    G = min(G, 255)
    B = min(B, 255)
    color = (R, G, B)
    screen.fill(color)
    # 1. Get the current time with decimals
    current_datetime = datetime.datetime.now()  
    # 2. Use .replace() to set microseconds to 0
    trimmed_datetime = current_datetime.replace(microsecond=0)
    time_string = trimmed_datetime.strftime("%H:%M:%S")
    current_minute = current_datetime.minute # Extract the minute (0 to 59)
    if 10 <= current_minute < 20:
        # Minutes 10-19: Orange
        COLOR = (255, 150, 0)
    elif 20 <= current_minute < 30:
        # Minutes 20-29: Yellow
        COLOR = (255, 255, 50)
    elif 30 <= current_minute < 40:
        # Minutes 30-39: Green
        COLOR = (50, 255, 50)
    elif 40 <= current_minute < 50:
        # Minutes 40-49: Cyan
        COLOR = (50, 255, 255)
    else: 
        # Minutes 50-59: Blue/Purple
        COLOR = (255, 255, 255)
    rendered_loading = font.render(time_string, True, COLOR)
    loading_rect = rendered_loading.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))  # Center dynamically
    screen.blit(rendered_loading, loading_rect)
    # Don't forget to update the display and handle events!
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
