import sys
from contacts import AddressBook, Record, Name, Phone, Birthday, Email
from notebook import Note, NoteBook
from datetime import datetime
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter, Completer, Completion
from prompt_toolkit.document import Document


class ConditionalCompleter(Completer):
    def __init__(self, completer, condition):
        self.completer = completer
        self.condition = condition

    def get_completions(self, document, complete_event):
        if self.condition(document):
            yield from self.completer.get_completions(document, complete_event)


# Список команд для автодополнения
COMMANDS = [
    "exit",
    "add_contact",
    "change_contact_phone",
    "show_all_contacts",
    "search_by_bd",
    "add_birthday",
    "add_email",
    "add_note",
    "search_note",
    "edit_note",
    "remove_not",
    "show_note",
    "help_note",
    "delete_contact",
    "search_contacts",
]
command_completer = WordCompleter(COMMANDS, ignore_case=True)


# Функция-условие, определяющая, когда активировать автодополнение
def completion_condition(document: Document):
    text_before_cursor = document.text_before_cursor
    return not text_before_cursor.strip().endswith(" ")


# Создание кастомного автодополнителя с условием
conditional_completer = ConditionalCompleter(command_completer, completion_condition)

# Создание сессии с автодополнением
session = PromptSession(completer=conditional_completer)


class ContactBot:
    def __init__(self, address_book, note_book):
        self.address_book = address_book
        self.note_book = note_book

    @staticmethod
    def hello():
        return "How can I help you?"

    # додавання контакту
    def add_contact(self, data):                         
        try:
            name, phone = data.split(maxsplit=1)
            record = Record(name)
            record.add_phone(Phone(phone))
            self.address_book.add_record(record)
            return f"Contact {name} added with phone {phone}"
        except ValueError:
            return "Invalid data format. Please provide both name and phone."

    # зміна номера телефону контакту
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

    # вивід всіх контактів
    def show_all_contacts(self):
        if not self.address_book.data:
            return "No contacts available"
        else:
            result = ""
            for record in self.address_book.data.values():
                birthday_info = ""
                birthday_datetime = record.birthday.value_as_datetime()
                if birthday_datetime:
                    days_to_birthday = record.days_to_birthday()
                    if days_to_birthday is None:
                        birthday_info = "None"
                    else:
                        birthday_info = f"{days_to_birthday} days left"
                else:
                    birthday_info = "None"
                result += f"Contact name: {record.name.value}, Phones: {', '.join(record.phones)}, Email: {record.email}, Birthday: {birthday_info}\n"
            return result

    # пошук контактів з днем народження в межах 14 днів
    def search_by_bd(self):
        upcoming_birthday_contacts = []
        today = datetime.today()
        for contact in self.address_book.data.values():
            if contact.birthday.value_as_datetime():
                next_birthday = datetime(today.year, contact.birthday.value_as_datetime().month, contact.birthday.value_as_datetime().day)
                if next_birthday < today:
                    next_birthday = datetime(today.year + 1, contact.birthday.value_as_datetime().month, contact.birthday.value_as_datetime().day)
                days_to_birthday = (next_birthday - today).days
                if 0 <= days_to_birthday <= 14:  
                    upcoming_birthday_contacts.append((contact, days_to_birthday))
        if not upcoming_birthday_contacts:
            return "No contacts with upcoming birthdays."
        else:
            result = ""
            for contact, days_left in upcoming_birthday_contacts:
                result += f"Contact: {contact.name.value.capitalize()}, Days until birthday: {days_left} ({contact.birthday})\n"  # Змінено
            return result

    # додавання дня народження контакту
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

    # додавання електронної адреси контакту
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
        title = input("Enter the title of the note:  ")
        text = input("Enter the content of the note: ")
        tags = input("Enter tags, separated by commas: ")
        new_note = Note(title, text, tags)                                          # Створення нової нотатки з усіма необхідними аргументами
        self.note_book.add_note(new_note)                                           # Додавання нової нотатки до нотатника
        return "Note added"

    def search_note(self, keyword): 
        return [note for note in self.notes if keyword.lower() in note.content.lower()]

    def edit_note(self, note_title, new_content):  # Пошук та редагування нотатки за назвою
        for note in self.note_book.data:
            if note.title == note_title:                                            # Порівнюємо назву нотатки з вказаною
                note.text = new_content                                             # Оновлюємо текст нотатки на новий зміст
                return "Note updated successfully."
        return "Note not found."

    def remove_note(self, note_title):
        pass

    def show_note(self):
        if not self.note_book.data:
            return "No notes available"
        else:
            return '\n'.join(str(note) for note in self.note_book.data)

    #надання користувачу довідки щодо доступних команд для роботи з нотатками
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

    #Видалення контакту 
    def delete_contact(self, name):
        self.address_book.delete(name)
        return f"Contact {name} deleted"

    #Пошук контакту 
    def search_contacts(self, name):
        found_records = [record for record in self.address_book.data.values() if name.lower() in record.name.value.lower() or any(name.lower() in phone.lower() for phone in record.phones)]
        if found_records:
            return "\n".join(str(record) for record in found_records)
        else:
            return f"No contacts found matching '{name}'"

    def main(self):
        while True:
            user_input = session.prompt("> ")
            #user_input = input("Enter command: ").lower()
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
            elif user_input.startswith("search_note"):  # + Шукає нотатки за певними ключовими словами і сортує від новішого до старішого до даті.
                search_query = user_input[len("search_note"):].strip()                                              # Отримуємо пошуковий запит, видаляючи команду та пробіли на початку та в кінці
                found_notes = note_book.search_note(search_query)
                for note in found_notes:
                    return note                                                                                     # Виводимо інформацію про кожну знайдену нотатку
            elif user_input.startswith("edit_note"):   # + Редагує існуючу нотатку. edit_note "назва рецепту" "новий зміст рецепту" 
                command, *args = user_input.split()                                                                 # Розділяємо введену команду на частини
                if len(args) >= 2:                                                                                  # Переконуємося, що користувач ввів ідентифікатор та новий зміст
                    note_id = args[0]                                                                               # Перше слово після команди - ідентифікатор нотатки
                    new_content = " ".join(args[1:])                                                                # Все інше - новий зміст нотатки
                    return self.edit_note(note_id, new_content)
                else:
                    return "Please, provide both an ID and new content for the note."
            elif user_input.startswith("remove_note"):  # + Видаляє нотаток.
                note_title = user_input[11:].strip()                                                                # Витягуємо назву нотатки і видаляємо зайві пробіли
                if self.note_book.remove_note_by_title(note_title):
                    return "Note removed successfully."
                else:
                    return "Note not found."
            elif user_input.startswith("remove_note"):
                data = user_input[11:].strip()                                                                      # Видаляємо команду та зайві пробіли
                return self.remove_note(data)
            elif user_input.startswith("show_note"):  # + Виводить список всіх нотаток.
                return self.show_note()
            elif user_input.startswith("help_note"):  # + Виводить список доступних команд для нотатника.
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
            elif user_input == "search_by_bd":
                return self.search_by_bd()
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
