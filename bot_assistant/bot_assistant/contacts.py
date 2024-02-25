import json
import re
from datetime import datetime
from collections import UserDict


class Field:
    def __init__(self, value):
        if not self.is_valid(value):
            raise ValueError("Invalid value")
        self.__value = value

    def __str__(self):
        return str(self.__value)

    def is_valid(self, value):
        return True

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if not self.is_valid(value):
            raise ValueError("Invalid value")
        self.__value = value


class Name(Field):
    pass


class Phone(Field):
    def is_valid(self, value):
        return len(value) == 10 and value.isdigit()

    def __init__(self, value):
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value=None):
        if value:
            self._validate_birthday_format(value)
        super().__init__(value)

    def _validate_birthday_format(self, value):
        date_today = datetime.now().date()
        if value.lower() != 'none':
            try:
                datetime.strptime(value, '%Y-%m-%d')
            except ValueError:
                raise ValueError
            if date_today < datetime.strptime(value, '%Y-%m-%d').date():
                raise ValueError
            else:
                return True

    def value_as_datetime(self):
        if self.value:
            if self.value.lower() == 'none':
                return None
            return datetime.strptime(self.value, '%Y-%m-%d')
        return None


class Email(Field):

    def __init__(self, value):
        super().__init__(value)

    def is_valid(self, value):
        if value is None:
            return True
        if isinstance(value, str):
            email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if re.match(email_regex, value):
                return True
        return False


class Record:
    def __init__(self, name, birthday=None, email=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday)
        self.email = Email(email)

    def add_phone(self, phone):
        self.phones.append(str(phone))

    def remove_phone(self, phone):
        self.phones.remove(phone)

    def edit_phone(self, old_phone, new_phone):
        index = self.phones.index(old_phone)
        self.phones[index] = new_phone

    def find_phone(self, phone):
        return phone in self.phones

    def days_to_birthday(self):
        if not self.birthday.value:
            return None
        today = datetime.today()
        next_birthday = datetime(today.year, self.birthday.value_as_datetime().month, self.birthday.value_as_datetime().day)
        if next_birthday < today:
            next_birthday = datetime(today.year + 1, self.birthday.value_as_datetime().month, self.birthday.value_as_datetime().day)
        delta = next_birthday - today
        return delta.days

    def __str__(self):
        phone_info = f"Phones: {', '.join(self.phones)}"
        email_info = f"Email: {self.email}" if self.email.value else "Email: None"
        birthday_info = f"Birthday: {self.birthday}" if self.birthday.value else "Birthday: None"
        return f"Contact name: {self.name.value}, {phone_info}, {email_info}, {birthday_info}"


class AddressBook(UserDict):
    def __init__(self, filename):
        self.filename = filename
        super().__init__()
        self.load_from_json()

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if len(name) <= 1:
            raise ValueError
        stripped_name = name.strip()
        if stripped_name in self.data:
            del self.data[stripped_name]
            print(f"Contact {stripped_name} deleted")
        else:
            print('no data found')

    def __iter__(self):
        return self.iterator()

    def iterator(self, part_record=1):
        records = list(self.data.values())
        num_records = len(records)
        current_index = 0
        while current_index < num_records:
            yield records[current_index:current_index + part_record]
            current_index += part_record

    def save_to_json(self):
        with open(self.filename, "w") as fh:
            json.dump([{"name": record.name.value,
                        "phones": record.phones,
                        "email": str(record.email),
                        "birthday": str(record.birthday)} for record in self.data.values()], fh, indent=4)

    def load_from_json(self):
        try:
            with open(self.filename, "r") as fh:
                data = json.load(fh)
                if not data:
                    return "The JSON file is empty."
                else:
                    self.data.clear()
                    for item in data:
                        record = Record(item['name'])
                        for phone in item['phones']:
                            record.add_phone(phone)
                        email_value = item['email']
                        if email_value.lower() == 'none':
                            email_value = None
                        record.email = Email(email_value)
                        birthday_value = item['birthday']
                        if birthday_value.lower() == 'none':
                            birthday_value = None
                        record.birthday = Birthday(birthday_value)
                        self.add_record(record)
        except FileNotFoundError:
            return "File not found. Creating a new address book."
