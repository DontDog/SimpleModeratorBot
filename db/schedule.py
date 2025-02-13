import csv
from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Session
from db.database import Base, DatabaseSession


def get_week_day_and_number(first_week_monday: str):
    # Преобразуем строку в объект datetime
    first_week_monday_date = datetime.strptime(first_week_monday, "%d.%m.%Y")

    # Текущая дата
    current_date = datetime.now()

    # Рассчитываем разницу между текущей датой и понедельником первой недели
    delta_days = (current_date - first_week_monday_date).days

    # Номер недели (нумерация с 1)
    week_number = delta_days // 7 + 1

    # День недели (0 - понедельник, 6 - воскресенье)
    day_of_week = current_date.weekday()  # Метод .weekday() возвращает день недели от 0 до 6 (0 - понедельник, 6 - воскресенье)

    return day_of_week, week_number

days_of_week = [
    "Пн",  # Понедельник
    "Вт",  # Вторник
    "Ср",  # Среда
    "Чт",  # Четверг
    "Пт",  # Пятница
    "Сб",  # Суббота
    "Вс"   # Воскресенье
]


class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True)
    week = Column(Integer, nullable=False)
    day = Column(Integer, nullable=False)
    room = Column(String, nullable=False)
    teacher = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="schedules")

    @classmethod
    def create(cls, user_id: int, week: int, day: int, room: str, teacher: str):
        with DatabaseSession() as db:
            schedule = cls(user_id=user_id, week=week, day=day, room=room, teacher=teacher)
            db.add(schedule)
            db.commit()
            db.refresh(schedule)
            return schedule

    @classmethod
    def get_by_user(cls, user_id: int):
        w, d = get_week_day_and_number('10.08.2025')
        with DatabaseSession() as db:
            return db.query(cls).filter(cls.user_id == user_id
                                        and cls.week == w and cls.day == days_of_week[d]).all()

    @classmethod
    def to_csv(cls, file_path: str):
        """Экспорт расписаний в CSV с разделителем табуляция."""
        with DatabaseSession() as db:
            schedules = db.query(cls).all()
            with open(file_path, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file, delimiter="\t")
                writer.writerow(["id", "week", "day", "room", "teacher", "user_id"])  # Заголовки
                for schedule in schedules:
                    writer.writerow([schedule.id, schedule.week, schedule.day, schedule.room, schedule.teacher, schedule.user_id])

    @classmethod
    def from_csv(cls, file_path: str):
        """Импорт расписаний из CSV с разделителем табуляция."""
        with DatabaseSession() as db:
            with open(file_path, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file, delimiter="\t")
                for row in reader:
                    schedule = cls(
                        id=int(row["id"]),
                        week=int(row["week"]),
                        day=int(row["day"]),
                        room=row["room"],
                        teacher=row["teacher"],
                        user_id=int(row["user_id"])
                    )
                    db.add(schedule)
                db.commit()
