import json
from datetime import datetime
from collections import UserList


class Note:
    def __init__(self, text):
        self.text = text
        self.creation_date = datetime.now()

    def __str__(self):
        return f"{self.creation_date}: {self.text}"


class NoteBook(UserList):
    def __init__(self, filename):
        self.filename = filename
        super().__init__()
        self.load_from_json()

    def add_note(self, note):
        self.data.append(note)

    def save_to_json(self):
        with open(self.filename, "w") as fh:
            json.dump([{"text": note.text, "creation_date": str(note.creation_date)} for note in self.data], fh, indent=4)

    def load_from_json(self):
        try:
            with open(self.filename, "r") as fh:
                data = json.load(fh)
                if not data:
                    return "The JSON file is empty."
                else:
                    self.data.clear()
                    for item in data:
                        note = Note(item['text'])
                        note.creation_date = datetime.strptime(item['creation_date'], '%Y-%m-%d %H:%M:%S.%f')
                        self.add_note(note)
        except FileNotFoundError:
            return "File not found. Creating a new note book."

