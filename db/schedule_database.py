import csv
import os
import pandas as pd
from datetime import datetime
from app.config import DATE_FIRST_LESSON


class ScheduleDatabase:
    def __init__(self, filename="schedule.csv"):
        self.filename = filename
        self.schedule = []
        self.first_monday = datetime.strptime(DATE_FIRST_LESSON,
                                              "%d.%m.%Y").date()  # Первая неделя будет привязана к понедельнику
        self._initialize_db()

    def _initialize_db(self):
        """Инициализация базы данных. Загружает данные из файла в список."""
        if os.path.exists(self.filename):
            with open(self.filename, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file, delimiter='\t')
                for row in reader:
                    self.schedule.append({
                        "week": int(row["week"]),
                        "day": row["day"],
                        "room": row["room"],
                        "teacher": row["teacher"]
                    })

        else:
            with open(self.filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter='\t')
                writer.writerow(["week", "day", "room", "teacher"])

    def get_current_week(self):
        """Возвращает текущий номер недели, начиная с первого понедельника."""
        if self.first_monday is None:
            raise ValueError("Первый понедельник не установлен.")

        # Получаем текущую дату
        today = datetime.now()

        # Преобразуем first_monday в datetime с 00:00:00 времени
        first_monday_datetime = datetime.combine(self.first_monday, datetime.min.time())

        # Разница между текущей датой и первым понедельником
        delta = today - first_monday_datetime

        # Номер текущей недели (целая часть от деления на 7 дней)
        current_week = (delta.days // 7) + 1
        return current_week

    def add_schedule_entry(self, week, day, room, teacher):
        """Добавляет новую запись в расписание."""
        self.schedule.append({"week": week, "day": day, "room": room, "teacher": teacher})
        self._save_to_csv()

    def _save_to_csv(self):
        """Сохраняет список расписания в CSV-файл."""
        with open(self.filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter='\t')
            writer.writerow(["week", "day", "room", "teacher"])
            for entry in self.schedule:
                writer.writerow([entry["week"], entry["day"], entry["room"], entry["teacher"]])

    def find_schedule(self, teacher, week=None, day=datetime.now().strftime("%A")):
        """Ищет расписание по номеру недели, дню недели и преподавателю."""
        if not week:
            week = self.get_current_week()
        return [entry for entry in self.schedule if
                entry["week"] == week and entry["day"] == day and entry["teacher"] == teacher]

    def get_teachers_by_day(self, week=None, day=datetime.now().strftime("%A")):
        """Возвращает список преподавателей и их аудиторий в указанный день недели."""
        if not week:
            week = self.get_current_week()
        return [{"teacher": entry["teacher"], "room": entry["room"]} for entry in self.schedule if
                entry["week"] == week and entry["day"] == day]

    def load_schedule_from_excel(self, excel_filename):
        """Заполняет базу данных расписания из Excel-файла. Ожидает, что название листа — это номер недели."""
        self.schedule = []

        day_map = {
            "Пн": "Monday",
            "Вт": "Tuesday",
            "Ср": "Wednesday",
            "Чт": "Thursday",
            "Пт": "Friday",
            "Сб": "Saturday"
        }

        # Загружаем все листы из файла
        sheets = pd.read_excel(excel_filename, sheet_name=None, index_col=0)

        for week, df in sheets.items():  # week — это название листа (номер недели)
            for room, row in df.iterrows():
                for day in day_map.keys():
                    if pd.notna(row[day]) and pd.notna(room):  # Проверяем, есть ли преподаватель в текущий день

                        self.add_schedule_entry(week, day_map[day], str(room), row[day])


if __name__ == "__main__":
    schedule_db = ScheduleDatabase()
    schedule_db.add_schedule_entry(1, "Monday", "101", "Dr. Smith")
    print(schedule_db.find_schedule("Dr. Smith", 1))
    print(schedule_db.get_teachers_by_day(1, "Monday"))
