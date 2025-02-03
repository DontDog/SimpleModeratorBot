import csv
import os

class UserDatabase:
    def __init__(self, filename="users.csv"):
        self.filename = filename
        self.users = {}
        self._initialize_db()

    def _initialize_db(self):
        """Инициализация базы данных. Загружает данные из файла в словарь."""
        if os.path.exists(self.filename):
            with open(self.filename, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file, delimiter='\t')
                for row in reader:
                    user_id = int(row["id"])
                    self.users[user_id] = {
                        "name": row["name"],
                        "full_name": row["full_name"],
                        "username": row["username"]
                    }
        else:
            with open(self.filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter='\t')
                writer.writerow(["id", "name", "full_name", "username"])

    def add_or_update_user(self, user_id, name, full_name, username):
        """Добавляет нового пользователя или обновляет его данные."""
        user_id = int(user_id)
        self.users[user_id] = {
            "name": name,
            "full_name": full_name,
            "username": username
        }
        self._save_to_csv()

    def _save_to_csv(self):
        """Сохраняет словарь пользователей в CSV-файл."""
        with open(self.filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter='\t')
            writer.writerow(["id", "name", "full_name", "username"])
            for user_id, data in self.users.items():
                writer.writerow([user_id, data["name"], data["full_name"], data["username"]])

    def get_user(self, user_id):
        """Получает данные пользователя по ID."""
        return self.users.get(int(user_id))

if __name__ == "__main__":
    db = UserDatabase()
    db.add_or_update_user(12345678, "Иван Иванов", "lol", "ivan_ivanov")
    print(db.get_user(12345678))