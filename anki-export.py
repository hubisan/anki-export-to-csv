import sqlite3
import csv
import os
import sys

# ----------------------------------------------------------------------
#                         *** KONFIGURATION ***
# ----------------------------------------------------------------------

# 1. Pfad zur Anki-Datenbank (collection.anki2) anpassen
#    Ersetzen Sie den Platzhalter durch Ihren tatsächlichen Pfad (z.B. den Snap-Pfad).
ANKI_DB_PATH = os.path.expanduser(
    "~/snap/anki-desktop/common/Hubisan/collection.anki2"
)

# 2. Felder auswählen, die exportiert werden sollen.
#    Die Indizes (0, 1, 2, ...) entsprechen der Reihenfolge der Felder in Ihrem Notiztyp.
#    Wenn Ihr Notiztyp "Vorderseite (0), Rückseite (1), Quelle (2)" hat:
FIELDS_TO_EXPORT = [0, 1, 2]

# 3. Header-Namen für die ausgewählten Felder festlegen (muss zur Anzahl der Indizes passen!)
FIELD_HEADERS = ["Vorderseite", "Rückseite", "Quelle"]

# ----------------------------------------------------------------------
#                        *** EXPORT-DETAILS ***
# ----------------------------------------------------------------------

# Name der Ausgabedatei
OUTPUT_FILE = "anki_custom_export.csv"

# Das interne Trennzeichen von Anki (Unit Separator, ASCII 31)
ANKI_FIELD_DELIMITER = chr(31)

# ----------------------------------------------------------------------
#                           *** FUNKTION ***
# ----------------------------------------------------------------------

def export_anki_notes():
    """Verbindet sich mit der DB, extrahiert Notizen/Metadaten und schreibt eine CSV-Datei."""
    
    if not os.path.exists(ANKI_DB_PATH):
        print(f"Fehler: Datenbankdatei nicht gefunden unter: {ANKI_DB_PATH}")
        print("Bitte den ANKI_DB_PATH im Skript anpassen und sicherstellen, dass Anki geschlossen ist.")
        sys.exit(1)

    print(f"Verbinde mit Datenbank: {ANKI_DB_PATH}")
    
    # Die Spalte flds (Feldinhalte) ist die letzte in der SQL-Abfrage.
    csv_headers = ["created_time_ms", "modified_time_sec", "tags"] + FIELD_HEADERS

    try:
        # Verbindung zur SQLite-Datenbank herstellen
        conn = sqlite3.connect(ANKI_DB_PATH)
        cursor = conn.cursor()

        # SQL-Abfrage: Holt ID (Erstellungszeit), mod (Änderungszeit), tags und flds
        query = "SELECT id, mod, tags, flds FROM notes"
        cursor.execute(query)
        
        # CSV-Datei zum Schreiben öffnen
        with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=';') # Verwenden Sie Semikolon als CSV-Trennzeichen

            # Header schreiben
            writer.writerow(csv_headers)

            # Zeilen verarbeiten und schreiben
            for row in cursor:
                id_ms, mod_sec, tags, flds_raw = row
                
                # Flds-String anhand des Anki-Trennzeichens aufteilen
                fields = flds_raw.split(ANKI_FIELD_DELIMITER)
                
                # Die gewünschten Feldinhalte auswählen
                selected_fields = [fields[i] for i in FIELDS_TO_EXPORT if i < len(fields)]
                
                # Die finale Zeile zusammenstellen: Metadaten + ausgewählte Felder
                output_row = [str(id_ms), str(mod_sec), tags.strip()] + selected_fields
                
                writer.writerow(output_row)

        print(f"\n✅ Export erfolgreich abgeschlossen.")
        print(f"Daten (nur ausgewählte Felder) wurden in '{OUTPUT_FILE}' geschrieben.")

    except sqlite3.OperationalError as e:
        print(f"\nFehler beim Datenbankzugriff: {e}")
        print("Mögliche Ursache: Anki ist geöffnet und sperrt die Datenbank.")
        sys.exit(1)
    except Exception as e:
        print(f"\nEin unerwarteter Fehler ist aufgetreten: {e}")
    finally:
        if 'conn' in locals() and conn:
            conn.close()

if __name__ == "__main__":
    export_anki_notes()
