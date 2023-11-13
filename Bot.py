def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Введіть ім'я користувача"
        except (ValueError, IndexError):
            return "Неправильні дані. Дайте ім'я та телефон, будь ласка."

    return wrapper

class AssistantBot:
    def __init__(self):
        self.contacts = {}

    @input_error
    def add_contact(self, command):
        _, name, phone = command.split()
        self.contacts[name] = phone
        return "Контакт успішно додано."

    @input_error
    def change_contact(self, command):
        _, name, phone = command.split()
        if name in self.contacts:
            self.contacts[name] = phone
            return "Контакт успішно оновлено."
        else:
            return "Контакт не знайдено."

    @input_error
    def show_contact(self, command):
        _, name = command.split()
        if name in self.contacts:
            return self.contacts[name]
        else:
            return "Контакт не знайдено."

    def show_all_contacts(self):
        if not self.contacts:
            return "Контакти не знайдено."
        result = "\n".join(f"{name}: {phone}" for name, phone in self.contacts.items())
        return result

def main():
    bot = AssistantBot()
    while True:
        command = input("Введіть команду: ").strip().lower()
        if command in ("good bye", "close", "exit"):
            print("Good bye!")
            break
        elif command == "hello":
            print("Чим я можу вам допомогти?")
        elif command.startswith("add"):
            print(bot.add_contact(command))
        elif command.startswith("change"):
            print(bot.change_contact(command))
        elif command.startswith("phone"):
            print(bot.show_contact(command))
        elif command == "show all":
            print(bot.show_all_contacts())
        else:
            print("Недійсна команда. Будь ласка спробуйте ще раз.")

if __name__ == "__main__":
    main()




