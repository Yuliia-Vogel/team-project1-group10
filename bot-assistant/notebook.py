import json
from datetime import datetime
from collections import UserList


class Note:
    def __init__(self, title, text, tags):
        self.title = title                  # Назва
        self.text = text                    # Зміст
        self.tags = tags.split(",")         # Теги
        self.creation_date = datetime.now() # сьогоднішня дата

    def __str__(self):
        return f"{self.creation_date}: {self.title} - {self.text}"


class NoteBook(UserList):
    def __init__(self, filename):
        self.filename = filename
        super().__init__()
        self.load_from_json()

    def add_note(self, note):
        self.append(note)

    def save_to_json(self):
        with open(self.filename, "w") as fh:
            json.dump([{"title": note.title, "text": note.text, "tags": note.tags, "creation_date": str(note.creation_date)} for note in self.data], fh, indent=4)

    def load_from_json(self):
        try:
            with open(self.filename, 'r') as file:
                notes_json = json.load(file)
                for note in notes_json:
                    # Припускаючи, що у JSON файлі для кожної нотатки є поля title, text і tags
                    self.data.append(Note(note['title'], note['text'], ','.join(note['tags'])))
        except FileNotFoundError:
            return "File not found. Creating a new note book."

