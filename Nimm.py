#!/usr/bin/env python3

import pygame
import sys
import math
import os
import random # Importiere random für die KI-Auswahl

# Initialisiere pygame
pygame.init()

# Sound initialisieren
pygame.mixer.init()
# Lade einen Soundeffekt
try:
    opponent_move_sound = pygame.mixer.Sound("opponent_move.wav")
except pygame.error as e:
    print(f"Warnung: Sounddatei 'opponent_move.wav' konnte nicht geladen werden: {e}")
    opponent_move_sound = None # Setze auf None, wenn Laden fehlschlägt

# Bildschirmgröße und Farben
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 128, 0) # Grün für die Regeln
BLUE = (0, 0, 150) # Dunkelblau für Erklärung
BUTTON_COLOR = (100, 100, 255)
BUTTON_TEXT_COLOR = WHITE

# Fenster erstellen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Naschkatze") # Geändert von Nimm-Spiel

# Schriftart
font = pygame.font.Font(None, 36)
button_font = pygame.font.Font(None, 30)
# Neue Schriftart für die Regeln (versucht, eine kursive und fette Systemschrift zu finden)
try:
    rules_font = pygame.font.SysFont('arial', 24, bold=True, italic=True) # Oder 'verdana', 'timesnewroman' etc.
except:
    print("Warnung: Kursive/Fette Systemschrift nicht gefunden, verwende Standard.")
    rules_font = pygame.font.Font(None, 24) # Fallback
    rules_font.set_bold(True)
    rules_font.set_italic(True)
# Neue Schriftart für die Erklärung am unteren Rand
explanation_font = pygame.font.Font(None, 22)


# Spielvariablen
candies = 18
candy_radius = 20
candy_spacing = 50
player_turn = True  # Spieler beginnt

# Schaltflächen definieren
button_width = 150
button_height = 50
button_y = HEIGHT - 100
button_spacing_x = 20
total_button_width = 3 * button_width + 2 * button_spacing_x
button_x_start = (WIDTH - total_button_width) // 2

button1_rect = pygame.Rect(button_x_start, button_y, button_width, button_height)
button2_rect = pygame.Rect(button_x_start + button_width + button_spacing_x, button_y, button_width, button_height)
button3_rect = pygame.Rect(button_x_start + 2 * (button_width + button_spacing_x), button_y, button_width, button_height)

# Texte
rules_text = "Regeln: Nimm 1, 2 oder 3 Zuckerl. Wer das letzte nimmt, verliert!" # Regeltext
explanation_text = "Klicke auf die Knöpfe, um Zuckerl zu nehmen. Versuche, den Computer das letzte Zuckerl nehmen zu lassen."

# Hilfsfunktion für Sprachausgabe
def speak(text):
    """Gibt den übergebenen Text über den 'say'-Befehl aus."""
    try:
        os.system(f"say -v Viktor '{text}'") # Warte bis 'say' fertig ist
    except Exception as e:
        print(f"Fehler beim Ausführen von 'say': {e}")

# Funktion zum Zeichnen der Bonbons in einem Quadrat
def draw_candies(candies_count):
    # screen.fill(WHITE) # Wird jetzt in der Hauptschleife gemacht
    cols = max(1, math.ceil(math.sqrt(candies_count)))  # Anzahl der Spalten im Quadrat, mindestens 1
    rows = math.ceil(candies_count / cols)  # Anzahl der Zeilen im Quadrat
    # Berechne Startpositionen, um Platz für Regeln und Erklärung zu lassen
    available_height = HEIGHT - 200 # Platz für Buttons, Regeln, Erklärung, Nachrichten
    candy_area_height = rows * candy_spacing
    y_offset = 120 # Platz für Titel, Regeln etc. oben
    x_start = (WIDTH - (cols * candy_spacing)) // 2  # Zentriere die Bonbons horizontal
    y_start = y_offset + (available_height - candy_area_height) // 2 # Zentriere vertikal im verfügbaren Bereich

    x, y = x_start, y_start
    for i in range(candies_count):
        pygame.draw.circle(screen, RED, (x, y), candy_radius)
        x += candy_spacing
        if (i + 1) % cols == 0:  # Nächste Zeile
            x = x_start
            y += candy_spacing

# Funktion zum Zeichnen von Schaltflächen
def draw_button(rect, text):
    pygame.draw.rect(screen, BUTTON_COLOR, rect, border_radius=10)
    label = button_font.render(text, True, BUTTON_TEXT_COLOR)
    label_rect = label.get_rect(center=rect.center)
    screen.blit(label, label_rect)

# Funktion zum Anzeigen von Text
def draw_text(text, x, y, color=BLACK, custom_font=None): # Parameter für benutzerdefinierte Schriftart
    f = custom_font if custom_font else font # Wähle Schriftart
    label = f.render(text, True, color)
    screen.blit(label, (x, y))

# Funktion zum Abspielen des Sounds für den gegnerischen Zug
def play_opponent_move_sound():
    if opponent_move_sound:
        opponent_move_sound.play()

# Funktion zum Anzeigen und Ansagen des Spielerzugs
def announce_player_move(move):
    message = f"Du hast {move} Zuckerl genommen. Verbleibende Zuckerl: {candies}"
    speak(message)

# Funktion zum Anzeigen und Ansagen des Computerzugs
def announce_computer_move(move):
    message = f"Computer hat {move} Zuckerl genommen. Verbleibende Zuckerl: {candies}"
    speak(message)

# Funktion zum Anzeigen des Spielendes
def announce_game_over(winner_message):
    screen.fill(WHITE)
    draw_text(winner_message, WIDTH // 2 - font.size(winner_message)[0] // 2, HEIGHT // 2 - 50)
    pygame.display.flip()
    speak(winner_message)
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()

# --- Spielstart ---
# Initiales Zeichnen des Fensters (vor der Sprachausgabe)
screen.fill(WHITE)
draw_candies(candies)
draw_text(f"Verbleibende Zuckerl: {candies}", 10, 10)
draw_text("Wähle 1, 2 oder 3 Zuckerl:", 10, 50)
draw_text(rules_text, 10, 90, color=GREEN, custom_font=rules_font)
draw_button(button1_rect, "1 Zuckerl")
draw_button(button2_rect, "2 Zuckerl")
draw_button(button3_rect, "3 Zuckerl")
explanation_label = explanation_font.render(explanation_text, True, GREEN) # Farbe auf Grün geändert
explanation_rect = explanation_label.get_rect(centerx=WIDTH // 2, bottom=HEIGHT - 10)
screen.blit(explanation_label, explanation_rect)
pygame.display.flip() # Fenster anzeigen

# Verarbeite Pygame-Ereignisse, um sicherzustellen, dass das Fenster gezeichnet wird
pygame.event.pump()
# Optional: Eine kleine Wartezeit kann zusätzlich helfen
# pygame.time.wait(50) # Warte 50 Millisekunden
# pygame.event.pump() # Erneut pumpen nach der Wartezeit

# Erklärung vorlesen (nachdem das Fenster sichtbar ist und Events verarbeitet wurden)
speak(explanation_text)


# Hauptspiel-Schleife
message_player = ""
message_computer = ""
game_over = False


while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and player_turn and not game_over:
            mouse_pos = event.pos
            move = 0
            # Prüfe, ob Buttons geklickt wurden und ob genügend Bonbons da sind
            if button1_rect.collidepoint(mouse_pos) and candies >= 1:
                move = 1
            elif button2_rect.collidepoint(mouse_pos) and candies >= 2:
                move = 2
            elif button3_rect.collidepoint(mouse_pos) and candies >= 3:
                move = 3

            if move > 0:
                candies -= move
                message_player = f"Du hast {move} Zuckerl genommen. Verbleibende Zuckerl: {candies}"
                message_computer = "" # Alte Computernachricht löschen
                try:
                    announce_player_move(move) # Ansage und Warten
                except Exception as e:
                    print(f"Fehler beim Aufruf von announce_player_move: {e}")

                player_turn = False
                # Überprüfen, ob Spieler verloren hat (Computer gewinnt)
                if candies == 0:
                    announce_game_over("Spiel vorbei! Der Computer hat gewonnen!")
                    game_over = True

    # KI-Zug (optimierte Strategie)
    if not player_turn and candies > 0 and not game_over:
        pygame.time.wait(500) # Kurze Pause für den Computerzug

        # Berechne den optimalen Zug
        remainder = candies % 4
        if remainder == 1:
            # Wenn candies % 4 == 1, kann der Computer nicht gewinnen, wenn der Spieler optimal spielt.
            # Er muss einen Zug machen (1, 2 oder 3). Wähle zufällig, um unvorhersehbar zu sein.
            ai_move = random.randint(1, min(3, candies))
        elif remainder == 2:
            ai_move = 1 # Nimm 1, um candies % 4 == 1 zu hinterlassen
        elif remainder == 3:
            ai_move = 2 # Nimm 2, um candies % 4 == 1 zu hinterlassen
        elif remainder == 0: # remainder == 0 (also candies % 4 == 0)
            ai_move = 3 # Nimm 3, um candies % 4 == 1 zu hinterlassen

        # Stelle sicher, dass der Zug gültig ist (sollte durch obige Logik abgedeckt sein, aber sicher ist sicher)
        ai_move = max(1, min(ai_move, 3, candies))

        candies -= ai_move
        play_opponent_move_sound()
        message_computer = f"Computer hat {ai_move} Zuckerl genommen. Verbleibende Zuckerl: {candies}"
        message_player = "" # Alte Spielernachricht löschen
        try:
            announce_computer_move(ai_move) # Ansage und Warten
        except Exception as e:
            print(f"Fehler beim Aufruf von announce_computer_move: {e}")

        player_turn = True
         # Überprüfen, ob Computer verloren hat (Spieler gewinnt)
        if candies == 0:
            announce_game_over("Spiel vorbei! Du hast gewonnen!")
            game_over = True

    if not game_over:
        # Zeichne den aktuellen Zustand
        screen.fill(WHITE) # Bildschirm zuerst leeren

        # Zeichne Bonbons
        draw_candies(candies)

        # Zeichne Texte
        draw_text(f"Verbleibende Zuckerl: {candies}", 10, 10)
        draw_text("Wähle 1, 2 oder 3 Zuckerl:", 10, 50)
        draw_text(rules_text, 10, 90, color=GREEN, custom_font=rules_font) # Regeln zeichnen

        # Zeichne Schaltflächen
        draw_button(button1_rect, "1 Zuckerl")
        draw_button(button2_rect, "2 Zuckerl")
        draw_button(button3_rect, "3 Zuckerl")

        # Zeige letzte Nachrichten an
        if message_player:
            draw_text(message_player, 10, HEIGHT - 60, color=GRAY, custom_font=explanation_font)
        if message_computer:
            draw_text(message_computer, 10, HEIGHT - 40, color=GRAY, custom_font=explanation_font)

        # Zeichne die Erklärung am unteren Rand
        explanation_label = explanation_font.render(explanation_text, True, GREEN) # Farbe auf Grün geändert
        explanation_rect = explanation_label.get_rect(centerx=WIDTH // 2, bottom=HEIGHT - 10) # Zentriert am unteren Rand
        screen.blit(explanation_label, explanation_rect)


        pygame.display.flip()

pygame.quit()
sys.exit()