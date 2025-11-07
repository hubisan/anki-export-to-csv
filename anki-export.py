import csv
import json
import re
import urllib.request
from datetime import datetime

ANKI_CONNECT_URL = "http://localhost:8765"

DECK_NAME = "Italienisch"
OUTPUT_FILE = "anki_exports/anki_export_italienisch.csv"

FIELDS_TO_EXPORT = [
    "native_language",
    "foreign_language",
    "foreign_language_phonetic",
    "foreign_language_literal",
    "foreign_language_usage_notes",
    "foreign_language_examples",
    "mnemonic",
]


def strip_html(text):
    """Entfernt einfache HTML-Tags wie <br> aus dem Text."""
    return re.sub("<[^>]*>", "", text)


def invoke(action, **params):
    """Anfrage an AnkiConnect senden"""
    req = json.dumps({"action": action, "version": 6, "params": params}).encode("utf-8")
    with urllib.request.urlopen(urllib.request.Request(ANKI_CONNECT_URL, req)) as res:
        return json.load(res)


def export_italienisch_notes():
    print(f"🔎 Suche Notizen im Deck '{DECK_NAME}*' ...")
    note_ids = invoke("findNotes", query=f'deck:"{DECK_NAME}*"')
    note_ids = note_ids.get("result", [])
    print(f"➡️  {len(note_ids)} Notizen gefunden.")

    if not note_ids:
        print("Keine Notizen gefunden – prüfe Decknamen oder AnkiConnect.")
        return

    notes_info = invoke("notesInfo", notes=note_ids)["result"]

    # Dateiname wurde angepasst, damit er nicht die vorherige Datei überschreibt
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        # 💡 WICHTIGE ÄNDERUNG: delimiter auf Komma (,) gesetzt.
        # QUOTE_ALL sorgt dafür, dass alle Felder, inkl. jener mit Kommas oder Zeilenumbrüchen,
        # korrekt in Anführungszeichen eingeschlossen werden.
        writer = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)

        header = ["created_time", "modified_time"] + FIELDS_TO_EXPORT
        writer.writerow(header)

        for note in notes_info:
            # Zeitstempel umwandeln
            created = datetime.fromtimestamp(note["noteId"] / 1000).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            modified = datetime.fromtimestamp(note["mod"] / 1000).strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            row = [created, modified]
            for field in FIELDS_TO_EXPORT:
                value = note["fields"].get(field, {}).get("value", "")

                # HTML-Bereinigung anwenden
                value = strip_html(value)

                row.append(value)
            writer.writerow(row)

    print(f"\n✅ Export abgeschlossen → {OUTPUT_FILE}")


if __name__ == "__main__":
    export_italienisch_notes()
