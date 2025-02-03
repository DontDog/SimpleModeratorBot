import csv
import os
import pandas as pd
import datetime

class ScheduleDatabase:
    def __init__(self, filename="schedule.csv"):
        self.filename = filename
        self.schedule = []
        self._initialize_db()

    def _initialize_db(self):
        """Инициализация базы данных. Загружает данные из файла в список."""
        if os.path.exists(self.filename):
            with open(self.filename, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file, delimiter='\t')
                for row in reader:
                    self.schedule.append({
                        "day": row["day"],
                        "room": row["room"],
                        "teacher": row["teacher"]
                    })
        else:
            with open(self.filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter='\t')
                writer.writerow(["day", "room", "teacher"])

    def add_schedule_entry(self, day, room, teacher):
        """Добавляет новую запись в расписание."""
        self.schedule.append({"day": day, "room": room, "teacher": teacher})
        self._save_to_csv()

    def _save_to_csv(self):
        """Сохраняет список расписания в CSV-файл."""
        with open(self.filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter='\t')
            writer.writerow(["day", "room", "teacher"])
            for entry in self.schedule:
                writer.writerow([entry["day"], entry["room"], entry["teacher"]])

    def find_schedule(self, teacher, day = datetime.datetime.now().strftime("%A")):
        """Ищет расписание по дню недели и преподавателю."""
        return [entry for entry in self.schedule if entry["day"] == day and entry["teacher"] == teacher]

    def get_teachers_by_day(self, day = datetime.datetime.now().strftime("%A")):
        """Возвращает список преподавателей и их аудиторий в указанный день недели."""
        return [{"teacher": entry["teacher"], "room": entry["room"]} for entry in self.schedule if entry["day"] == day]

    def load_schedule_from_excel(self, excel_filename):
        """Заполняет базу данных расписания из Excel-файла."""
        df = pd.read_excel(excel_filename, index_col=0)

        day_map = {
            "Пн": "Monday",
            "Вт": "Tuesday",
            "Ср": "Wednesday",
            "Чт": "Thursday",
            "Пт": "Friday",
            "Сб": "Saturday"
        }

        self.schedule = []
        for room, row in df.iterrows():
            for day in day_map.keys():
                if pd.notna(row[day]):  # Проверяем, есть ли преподаватель в текущий день
                    self.add_schedule_entry(day_map[day], str(room), row[day])

if __name__ == "__main__":
    schedule_db = ScheduleDatabase()
    schedule_db.add_schedule_entry("Monday", "101", "Dr. Smith")
    print(schedule_db.find_schedule("Dr. Smith"))
    print(schedule_db.get_teachers_by_day("Monday"))