from collections import UserDict
from datetime import datetime, timedelta
import re
import pickle

class Field:
    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        super().__init__(value)
        self.validate()

    def validate(self):
        if not self.value:
            raise ValueError("Назва не може бути пустою")

class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        self.validate()

    def validate(self):
        if self.value is not None and not re.match(r'^\d{10}$', str(self.value)):
            raise ValueError("Недійсний формат номера телефону. Він повинен містити 10 цифр.")

class Birthday(Field):
    def __init__(self, value=None):
        super().__init__(value)
        self.validate()

    def validate(self):
        if self.value is not None:
            try:
                datetime.strptime(str(self.value), '%Y-%m-%d')
            except ValueError:
                raise ValueError("Недійсний формат дня народження. Використовуйте формат 'YYYY-MM-DD'.")


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birhday = Birthday(birthday)

    def __str__(self):
        phones_str = '; '.join(str(phone) for phone in self.phones)
        birthday_str = f", день народження: {self.birthday}" if self.birthday.value else ""
        return f"Контактна особа: {self.name}{birthday_str}, телефони: {phones_str}"

    def days_to_birthday(self):
        if self.birthday.value:
            today = datetime.now()
            next_birthday = datetime(today.year, self.birthday.value.month, self.birthday.value.day)
            if today > next_birthday:
                next_birthday = datetime(today.year + 1, self.birthday.value.month, self.birthday.value.day)
            days_left = (next_birthday - today).days
            return days_left
        return None

    @property
    def birthday(self):
        return self._birthday

    @birthday.setter
    def birthday(self, value):
        self._birthday = Birthday(value)



    def add_phone(self, phone):
        phone_obj = Phone(phone)
        self.phones.append(phone_obj)

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if str(p) != str(phone)]

    def edit_phone(self, old_phone, new_phone):
        if old_phone in [str(phone) for phone in self.phones]:
            for phone in self.phones:
                if str(phone) == old_phone:
                    phone.value = new_phone
            print(f"Телефон {old_phone} успішно оновлено до {new_phone}.")
        else:
            raise ValueError(f"Телефон {old_phone} не знайдено в записі.")

    def find_phone(self, phone):
        return next((p for p in self.phones if str(p) == str(phone)), None)

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[str(record.name)] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]


    # DZ11
    def iterator(self, page_size=5):
        records = list(self.data.values())
        total_records = len(records)
        start = 0
        while start < total_records:
            yield records[start:start+page_size]
            start += page_size




    # DZ12

    def save_to_disk(self, filename="address_book.pkl"):
        with open(filename, 'wb') as file:
            pickle.dump(self.data, file)

    def load_from_disk(self, filename="address_book.pkl"):
        try:
            with open(filename, 'rb') as file:
                self.data = pickle.load(file)
        except FileNotFoundError:
            print("Файл не знайдено. Створюємо новий об'єкт AddressBook.")
            self.data = {}


    def search(self, query):
        results = []
        for record in self.data.values():
            if query.lower() in str(record.name).lower() or any(query in str(phone) for phone in record.phones):
                results.append(record)
        return results





# # Створення нової адресної книги
# book = AddressBook()
#
# # Створення запису для John
# john_record = Record("John")
# john_record.add_phone("1234567890")
# john_record.add_phone("5555555555")
#
# # Додавання запису John до адресної книги
# book.add_record(john_record)
#
# # Створення та додавання нового запису для Jane
# jane_record = Record("Jane")
# jane_record.add_phone("9876543210")
# book.add_record(jane_record)
#
# # Виведення всіх записів у книзі
# for name, record in book.data.items():
#     print(record)
#
# # Знаходження та редагування телефону для John
# john = book.find("John")
# john.edit_phone("1234567890", "1112223333")
#
# print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555
#
# # Пошук конкретного телефону у записі John
# found_phone = john.find_phone("5555555555")
# print(f"{john.name}: {found_phone}")  # Виведення: 5555555555
#
# # Видалення запису Jane
# book.delete("Jane")





# Створюємо об'єкт AddressBook
# address_book = AddressBook()
#
# # Додаємо записи
# record1 = Record(name="John Doe", birthday="1990-05-15")
# record1.add_phone("1234567890")
# record1.add_phone("9876543210")
#
# record2 = Record(name="Jane Doe", birthday="1985-08-20")
# record2.add_phone("5551112233")
#
# address_book.add_record(record1)
# address_book.add_record(record2)
#
# # Зберігаємо на диск
# address_book.save_to_disk()
#
# # Відновлюємо з диска
# address_book.load_from_disk()
#
# # Пошук за ім'ям чи номером телефону
# search_results = address_book.search("Doe")
# for result in search_results:
#     print(result)