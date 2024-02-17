import sys
from contacts import AddressBook, Record, Name, Phone, Birthday, Email
from notebook import Note, NoteBook


class ContactBot:
    def __init__(self, address_book, note_book):
        self.address_book = address_book
        self.note_book = note_book

    @staticmethod
    def hello():
        return "How can I help you?"

    def add_contact(self, data):
        try:
            name, phone = data.split(maxsplit=1)
            record = Record(name)
            record.add_phone(Phone(phone))
            self.address_book.add_record(record)
            return f"Contact {name} added with phone {phone}"
        except ValueError:
            return "Invalid data format. Please provide both name and phone."

    def change_contact_phone(self, data):
        try:
            name, phone = data.split(maxsplit=1)
            record = self.address_book.find(name)
            if record:
                record.phones.clear()
                record.add_phone(Phone(phone))
                return f"Phone number updated for {name}"
            else:
                return "Contact not found"
        except ValueError:
            return "Invalid data format. Please provide both name and phone."

    def show_all_contacts(self):
        if not self.address_book:
            return "No contacts available"
        else:
            result = "\n".join(str(record) for record in self.address_book.data.values())
            return result

    def add_birthday(self, data):
        try:
            name, birthday = data.split(maxsplit=1)
            if name in self.address_book:
                self.address_book[name].birthday = Birthday(birthday)
                return f"Birthday added for {name}"
            else:
                return f"Contact with name {name} does not exist."
        except ValueError:
            return "Invalid data format. Please provide both name and birthday."

    def add_email(self, data):
        try:
            name, email = data.split(maxsplit=1)
            if name and email:
                if name in self.address_book:
                    self.address_book[name].email = Email(email)
                    return f"Email added for {name}"
                else:
                    return f"Contact with name {name} does not exist."
            else:
                return "Invalid data format. Please provide both name and email."
        except ValueError:
            return "Invalid data format. Please provide both name and email."

    def add_note(self):
        title = input("Введіть назву нотатки: ")
        text = input("Введіть зміст нотатки: ")
        tags = input("Введіть теги, розділені комою: ")
        new_note = Note(title, text, tags)  # Створення нової нотатки з усіма необхідними аргументами
        self.note_book.add_note(new_note)  # Додавання нової нотатки до нотатника
        return "Note added"

    def search_note(self, keyword):
        return [note for note in self.notes if keyword.lower() in note.content.lower()]

    def edit_note(self, id, new_content):
        for note in self.notes:
            if note.id == id:
                note.content = new_content
                return "Note updated"
        return "Note not found"

    def remove_note(self, id):
        for note in self.notes:
            if note.id == id:
                self.notes.remove(note)
                return "Note removed"
        return "Note not found"

    def show_note(self):
        if not self.note_book:
            return "No notes available"
        else:
            return '\n'.join(str(note) for note in self.note_book)

    def help_note(self):
        commands = {
            "add_note": "Add a new note. Usage: add_note your note here",
            "search_note": "Search notes by keyword. Usage: search_note keyword",
            "edit_note": "Edit an existing note. Usage: edit_note id new content",
            "remove_note": "Remove a note. Usage: remove_note id",
            "show_note": "Show all notes.",
            "help_note": "Show this help message."
        }
        return '\n'.join([f"{cmd}: {desc}" for cmd, desc in commands.items()])

    def delete_contact(self, name):
        self.address_book.delete(name)
        return f"Contact {name} deleted"

    def search_contacts(self, name):
        found_records = [record for record in self.address_book.data.values() if name.lower() in record.name.value.lower() or any(name.lower() in phone.lower() for phone in record.phones)]
        if found_records:
            return "\n".join(str(record) for record in found_records)
        else:
            return f"No contacts found matching '{name}'"

    def main(self):
        while True:
            user_input = input("Enter command: ").lower()
            if user_input in ["good bye", "close", "exit", "."]:
                self.address_book.save_to_json()
                self.note_book.save_to_json()
                return exit_bot()
            elif user_input.startswith("add_birthday"):
                data = user_input[len("add_birthday")+1:]
                return self.add_birthday(data)
            elif user_input.startswith("add_email"):
                data = user_input[len("add_email")+1:]
                return self.add_email(data)
            elif user_input == "hello":
                return self.hello()
            elif user_input.startswith("add_contact"):
                data = user_input[11:]
                return self.add_contact(data)
            elif user_input.startswith("add_note"):  # + Додає нотатку до нотатника. 
                return self.add_note()
            elif user_input.startswith("search_note"): # - Шукає нотатки за певними ключовими словами.
                data = user_input[11:]
                return self.search_note(data)
            elif user_input.startswith("edit_note"): # - Редагує існуючу нотатку.
                data = user_input[9:]
                return self.edit_note(data)
            elif user_input.startswith("remove_note"): # - Видаляє нотатку.
                data = user_input[11:]
                return self.remove_note(data)
            elif user_input.startswith("show_note"): # + Виводить список всіх нотаток.
                return self.show_note()
            elif user_input.startswith("help_note"): # + Виводить список доступних команд для нотатника.
                return self.help_note()

            elif user_input.startswith("change_contact_phone"):
                data = user_input[len("change_contact_phone")+1:]
                return self.change_contact_phone(data)
            elif user_input == "show all":
                return self.show_all_contacts()
            elif user_input.startswith("delete_contact"):
                name = user_input[14:]
                return self.delete_contact(name)
            elif user_input.startswith("search_contacts"):
                name = user_input[16:]
                return self.search_contacts(name)
            else:
                return "Invalid command. Try again."


def exit_bot() -> None:
    print("Good bye!")
    sys.exit()


if __name__ == "__main__":
    address_book = AddressBook("address_book.json")
    note_book = NoteBook("notes.json")
    bot = ContactBot(address_book, note_book)
    while True:
        print(bot.main())
