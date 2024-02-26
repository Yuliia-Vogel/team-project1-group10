import json
from datetime import datetime
from collections import UserList


class Note:
    def __init__(self, title, text, tags):
        self.title = title                   # Назва
        self.text = text                     # Зміст
        self.tags = tags.split(",")          # Теги
        self.creation_date = datetime.now()  # сьогоднішня дата

    def __str__(self):
        return f"{self.creation_date}\n- {self.title}\n- {self.text}\n- {self.tags}"


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

    def remove_note_by_title(self, title):
        for i, note in enumerate(self.data):
            if note.title.lower() == title:
                del self.data[i]
                return True
        return False

    def search_note(self, search_query):
        search_terms = search_query.lower().split()  # Розбиваємо пошуковий запит на слова
        found_notes = [
            note
            for note in self.data
            if any(term in note.title.lower() or term in note.text.lower() or term in ' '.join(note.tags).lower() for term in search_terms)
        ]
        if found_notes:
            return "\n".join(str(note) for note in found_notes)
        else:
            return "No notes found matching '{search_query}'"

    def load_from_json(self):
        try:
            with open(self.filename, "r") as fh:
                data = json.load(fh)
                if not data:
                    return "The JSON file is empty."
                else:
                    self.data.clear()
                    for item in data:
                        note = Note(item['title'], item['text'], ','.join(item['tags']))
                        note.creation_date = datetime.strptime(item['creation_date'], '%Y-%m-%d %H:%M:%S.%f')
                        self.add_note(note)  # Додаємо об'єкт note до списку
        except FileNotFoundError:
            return "File not found. Creating a new note book."
