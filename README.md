```markdown
```markdown
# Nimm Projekt Dokumentation

## Übersicht

Das Nimm-Projekt besteht aus zwei Hauptkomponenten: `Nimm.html` und `Nimm.py`. Diese README bietet eine Übersicht über deren Funktionalität und Nutzung.

## Nimm.py

`Nimm.py` ist ein Python-Skript, das die Logik für das Nimm-Spiel implementiert. Es enthält Funktionen zur Handhabung der Spielmechanik, wie Spielerzüge, Zugvalidierung und die Bestimmung des Gewinners.

### Hauptfunktionen

- **Spielmechanik**  
    Diese Funktionen ermöglichen die Durchführung des Spiels, einschließlich der Verwaltung der verbleibenden Objekte und der Überprüfung der Spielregeln.

    ```python
    def make_move(objects, take):
        """
        Führt einen Spielzug aus, indem eine bestimmte Anzahl von Objekten entfernt wird.

        Args:
            objects (int): Die aktuelle Anzahl der Objekte im Spiel.
            take (int): Die Anzahl der zu entfernenden Objekte.

        Returns:
            int: Die verbleibende Anzahl der Objekte nach dem Zug.

        Raises:
            ValueError: Wenn die Anzahl der zu entfernenden Objekte ungültig ist.
        """
        if take <= 0 or take > objects:
            raise ValueError("Ungültiger Zug. Anzahl der zu entfernenden Objekte muss zwischen 1 und der verbleibenden Anzahl liegen.")
        return objects - take
    ```

## Nimm.html

`Nimm.html` bietet die Benutzeroberfläche für das Nimm-Spiel. Es ermöglicht Spielern, über einen Webbrowser mit dem Spiel zu interagieren. Die HTML-Datei enthält Buttons, Eingabefelder und visuelle Elemente, um die Benutzererfahrung zu verbessern.

### Funktionen

- Interaktive Benutzeroberfläche für das Nimm-Spiel.
- Echtzeit-Updates, um den aktuellen Spielstatus anzuzeigen.
- Responsives Design für die Kompatibilität mit verschiedenen Geräten.

## Nutzung

1. Klonen Sie das Repository:
     ```bash
     git clone https://github.com/yourusername/Nimm.git
     ```
2. Führen Sie das Python-Skript aus:
     ```bash
     python Nimm.py
     ```
3. Öffnen Sie `Nimm.html` in einem Webbrowser, um das Spiel zu starten.

## Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert. Details finden Sie in der Datei `LICENSE`.
```