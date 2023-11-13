from collections import UserDict
import re

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

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def __str__(self):
        phones_str = '; '.join(str(phone) for phone in self.phones)
        return f"Контактна особа: {self.name}, телефони: {phones_str}"

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