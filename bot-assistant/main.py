import sys
from contacts import AddressBook, Record, Name, Phone, Birthday, Email
from notebook import Note, NoteBook
from datetime import datetime


def exit_bot() -> None:
    print("Good bye!")
    sys.exit()


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

    def add_note(self, note):
        self.note_book.add_note(Note(note))
        return "Note added"

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
        
    def search_by_bd(self):
        upcoming_birthday_contacts = []
        today = datetime.today()
        for contact in self.address_book.data.values():
            if contact.birthday.value_as_datetime():
                next_birthday = datetime(today.year, contact.birthday.value_as_datetime().month, contact.birthday.value_as_datetime().day)
                if next_birthday < today:
                    next_birthday = datetime(today.year + 1, contact.birthday.value_as_datetime().month, contact.birthday.value_as_datetime().day)
                days_to_birthday = (next_birthday - today).days
                if 0 <= days_to_birthday <= 7:  
                    upcoming_birthday_contacts.append((contact, days_to_birthday))
        if not upcoming_birthday_contacts:
            return "No contacts with upcoming birthdays."
        else:
            result = ""
            for contact, days_left in upcoming_birthday_contacts:
                result += f"Contact: {contact.name.value}, Days until birthday: {days_left}\n"
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
            elif user_input.startswith("add_note"):
                data = user_input[8:]
                return self.add_note(data)
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
                 print(self.search_by_bd())
            else:
                return "Invalid command. Try again."


if __name__ == "__main__":
    address_book = AddressBook("address_book.json")
    note_book = NoteBook("notes.json")
    bot = ContactBot(address_book, note_book)
    while True:
        print(bot.main())
