# Anki to CSV Export Script (via AnkiConnect)

This Python script exports **notes from Anki** into a structured **CSV file** using the [AnkiConnect](https://foosoft.net/projects/anki-connect/) API.
It’s designed for flexible use — you can export _any deck_ and _any note type_ by simply adjusting the deck name, fields, and output file.

Originally created for an Italian vocabulary deck, it can easily be reused for other decks and languages.

---

## Overview

The script connects to a running Anki instance (via AnkiConnect on `localhost:8765`), retrieves all notes from a given deck, extracts selected fields, removes basic HTML, and writes everything into a clean UTF-8 CSV file.

## Requirements

1. **Anki Desktop** installed
   [https://apps.ankiweb.net](https://apps.ankiweb.net)

2. **AnkiConnect Add-on** installed and enabled

   - In Anki: `Tools → Add-ons → Get Add-ons`
   - Code: **2055492159**
   - Restart Anki afterward.

3. **Python 3.8+** installed
   - Check with:
     ```bash
     python --version
     ```

## Usage

1. Make sure **Anki Desktop** is running.
   The script communicates with Anki via `http://localhost:8765`.

2. Run the export script:

   ```bash
   python export_anki_to_csv.py
   ```

3. The resulting file will be created here (or wherever you configure it):
   ```
   anki_exports/anki_export.csv
   ```

## Configuration

The script uses a few constants you should customize:

```python
ANKI_CONNECT_URL = "http://localhost:8765"
DECK_NAME = "Italienisch"  # Change this to match your deck
OUTPUT_FILE = "anki_exports/anki_export_italienisch.csv"

FIELDS_TO_EXPORT = [
    "native_language",
    "foreign_language",
    "foreign_language_examples",
    # Add or remove fields depending on your note type
]
```

| Setting            | Description                                                               |
| ------------------ | ------------------------------------------------------------------------- |
| `DECK_NAME`        | Name of the deck you want to export. Must exactly match the name in Anki. |
| `FIELDS_TO_EXPORT` | List of field names from your note type to include in the CSV.            |
| `OUTPUT_FILE`      | Path and filename of the resulting CSV file.                              |

> You can find your note type’s field names in Anki:
> `Tools → Manage Note Types → Fields…`

## What the Script Does

### `strip_html(text)`

Removes simple HTML tags like `<br>` from note fields to make the CSV output cleaner.

### `invoke(action, **params)`

Handles communication with AnkiConnect via HTTP POST requests.
Examples of actions: `findNotes`, `notesInfo`, `addNote`, etc.

### `export_italienisch_notes()`

_(You can rename this function to something like `export_notes()` if you wish)_

- Searches for all notes in the specified deck
- Fetches field data for each note
- Removes HTML formatting
- Converts timestamps to readable dates
- Writes a UTF-8 CSV with comma delimiter and full quoting (`QUOTE_ALL`)

## Example Output

```csv
"created_time","modified_time","native_language","foreign_language","foreign_language_examples"
"2025-11-06 14:12:00","2025-11-06 14:15:30","I would like","vorrei","Vorrei un caffè, per favore.<br>I would like a coffee, please."
```

The output is suitable for further processing or backup. You can re-import it into spreadsheets or other systems easily.

## Example Customization

```python
DECK_NAME = "French Basics"
OUTPUT_FILE = "anki_exports/french_export.csv"
FIELDS_TO_EXPORT = ["front", "back", "example_sentence"]
```

This would export a French deck with your chosen fields.

## License

This project is licensed under the **GNU General Public License v3.0 (GPL-3.0)**.

You are free to use, modify, and distribute this software as long as derivative works are also licensed under GPL-3.0.
