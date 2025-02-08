import csv
import os
from datetime import datetime, time
from app.config import PRESENCE_CHECK_START, PRESENCE_CHECK_END

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
                        "username": row["username"],
                        "last_checked": row["last_checked"]
                    }
        else:
            with open(self.filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter='\t')
                writer.writerow(["id", "name", "full_name", "username", "last_checked"])

    def add_or_update_user(self, user_id, name, full_name, username):
        """Добавляет нового пользователя или обновляет его данные."""
        user_id = int(user_id)

        self.users[user_id] = {
            "name": name,
            "full_name": full_name,
            "username": username,
            "last_checked": "None"
        }
        self._save_to_csv()

    def update_last_checked(self, user_id):
        """Обновляет время последнего отмечания пользователя."""
        if user_id in self.users:
            self.users[user_id]["last_checked"] = datetime.now().strftime("%A, %Y-%m-%d %H:%M:%S")
            self._save_to_csv()

    def _save_to_csv(self):
        """Сохраняет словарь пользователей в CSV-файл."""
        with open(self.filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter='\t')
            writer.writerow(["id", "name", "full_name", "username", "last_checked"])
            for user_id, data in self.users.items():
                writer.writerow([user_id, data["name"], data["full_name"], data["username"], data["last_checked"]])

    def get_user(self, user_id):
        """Получает данные пользователя по ID."""
        return self.users.get(int(user_id))

    def check_user_by_full_name(self, full_name):
        """Проверяет, был ли пользователь с таким ФИО обновлен сегодня с 7 до 9 часов."""
        today = datetime.now().date()
        ps = PRESENCE_CHECK_START.split(':')
        pe = PRESENCE_CHECK_END.split(':')
        start_time = datetime.combine(today, time(int(ps[0]), int(ps[1])))
        end_time = datetime.combine(today, time(int(pe[0]), int(pe[1])))

        # Ищем пользователей с таким ФИО
        for user_id, data in self.users.items():
            if data["name"] == full_name:
                # Проверяем, было ли обновление сегодня и в указанном времени
                if data["last_checked"] != "None":
                    last_checked = datetime.strptime(data["last_checked"], "%A, %Y-%m-%d %H:%M:%S")
                    if start_time <= last_checked <= end_time:
                        return True
        return False


if __name__ == "__main__":
    db = UserDatabase()
    db.add_or_update_user(12345678, "Иван Иванов", "lol", "ivan_ivanov")
    print(db.get_user(12345678))