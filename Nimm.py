import pygame
import sys
import math
import os

# Initialisiere pygame
pygame.init()

# Sound initialisieren
pygame.mixer.init()
# Lade einen Soundeffekt
opponent_move_sound = pygame.mixer.Sound("opponent_move.wav")

# Bildschirmgröße und Farben
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Fenster erstellen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Nimm-Spiel")

# Schriftart
font = pygame.font.Font(None, 36)

# Spielvariablen
candies = 18
candy_radius = 20
candy_spacing = 50
candy_y = HEIGHT // 2
player_turn = True  # Spieler beginnt

# Funktion zum Zeichnen der Bonbons in einem Quadrat
def draw_candies(candies):
    screen.fill(WHITE)
    cols = max(1, math.ceil(math.sqrt(candies)))  # Anzahl der Spalten im Quadrat, mindestens 1
    rows = math.ceil(candies / cols)  # Anzahl der Zeilen im Quadrat
    x_start = (WIDTH - (cols * candy_spacing)) // 2  # Zentriere die Bonbons horizontal
    y_start = (HEIGHT - (rows * candy_spacing)) // 2  # Zentriere die Bonbons vertikal

    x, y = x_start, y_start
    for i in range(candies):
        pygame.draw.circle(screen, RED, (x, y), candy_radius)
        x += candy_spacing
        if (i + 1) % cols == 0:  # Nächste Zeile
            x = x_start
            y += candy_spacing

# Funktion zum Anzeigen von Text
def draw_text(text, x, y):
    label = font.render(text, True, BLACK)
    screen.blit(label, (x, y))

# Funktion zum Anzeigen des gegnerischen Zugs
def draw_opponent_move(move):
    draw_text(f"Gegner nimmt {move} Zuckerl", 10, 90)
    if candies == 0:
        draw_text("Spiel vorbei! Gegner hat gewonnen!", 200, 300)
        os.system("say 'Spiel vorbei! Gegner hat gewonnen!'")

# Funktion zum Abspielen des Sounds für den gegnerischen Zug
def play_opponent_move_sound():
    opponent_move_sound.play()

# Funktion zum Anzeigen und Ansagen des Spielerzugs
def announce_player_move(move):
    draw_text(f"Du hast {move} Zuckerl genommen", 10, 130)
    os.system(f"say -v Viktor 'Du hast {move} Zuckerl genommen'")

# Funktion zum Anzeigen und Ansagen des Computerzugs
def announce_computer_move(move):
    draw_text(f"Computer hat {move} Zuckerl genommen", 10, 170)
    os.system(f"say 'Computer hat {move} Zuckerl genommen'")

# Hauptspiel-Schleife (angepasst für Gegnerzug-Anzeige)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN and player_turn:
            if event.key == pygame.K_1 and candies >= 1:
                candies -= 1
                announce_player_move(1)  # Zeige und sage den Spielerzug an
                player_turn = False
            elif event.key == pygame.K_2 and candies >= 2:
                candies -= 2
                announce_player_move(2)  # Zeige und sage den Spielerzug an
                player_turn = False
            elif event.key == pygame.K_3 and candies >= 3:
                candies -= 3
                announce_player_move(3)  # Zeige und sage den Spielerzug an
                player_turn = False

    # Überprüfen, ob das Spiel vorbei ist
    if candies == 0:
        screen.fill(WHITE)
        draw_text("Spiel vorbei! Du hast gewonnen!", 200, 300)
        pygame.display.flip()
        pygame.time.wait(3000)
        pygame.quit()
        sys.exit()

    # KI-Zug (optimierte Strategie)
    if not player_turn and candies > 0:
        ai_move = (candies - 1) % 4  # Versuche, die Bonbons auf ein Vielfaches von 4 zu reduzieren
        if ai_move == 0 or ai_move > candies:
            ai_move = min(3, candies)  # Falls nicht möglich, nimm so viele wie möglich (max. 3)
        candies -= ai_move
        draw_opponent_move(ai_move)  # Zeige den Zug des Gegners an
        play_opponent_move_sound()  # Spiele den Sound ab
        announce_computer_move(ai_move)  # Zeige und sage den Computerzug an
        player_turn = True

    # Zeichne den aktuellen Zustand
    draw_candies(candies)
    draw_text(f"Verbleibende Zuckerl: {candies}", 10, 10)
    draw_text("Drücke 1, 2 oder 3, um Zuckerl zu nehmen.", 10, 50)
    pygame.display.flip()