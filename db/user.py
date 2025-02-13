import csv
from datetime import datetime
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.database import Base, DatabaseSession

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    username = Column(String, nullable=True)
    telegram_id = Column(Integer, unique=True, nullable=False)  # Новый столбец
    last_checked = Column(String, nullable=True)

    schedules = relationship("Schedule", back_populates="user", cascade="all, delete-orphan")

    @classmethod
    def create(cls, name: str, full_name: str, username: str, telegram_id: int = None, last_checked: str = None):
        """Создает нового пользователя."""
        with DatabaseSession() as db:
            user = cls(name=name, full_name=full_name, username=username,
                       telegram_id=telegram_id, last_checked=last_checked)
            db.add(user)
            db.commit()
            db.refresh(user)
            return user


    @classmethod
    def update_user(cls, user_id: int, name: str = None, full_name: str = None, username: str = None, telegram_id: int = None, last_checked: str = None):
        """Обновляет данные пользователя по ID."""
        with DatabaseSession() as db:
            user = db.query(cls).filter(cls.id == user_id).first()
            if user:
                if name:
                    user.name = name
                if full_name:
                    user.full_name = full_name
                if username:
                    user.username = username
                if telegram_id is not None:
                    user.telegram_id = telegram_id
                if last_checked:
                    user.last_checked = last_checked
                db.commit()  # Сохраняем изменения
                db.refresh(user)  # Обновляем объект с новыми данными
                return user
            return None

    @classmethod
    def get_by_id(cls, user_id: int):
        """Получает пользователя по ID."""
        with DatabaseSession() as db:
            return db.query(cls).filter(cls.id == user_id).first()

    @classmethod
    def get_by_telegram_id(cls, telegram_id: int):
        """Получает пользователя по Telegram ID."""
        with DatabaseSession() as db:
            return db.query(cls).filter(cls.telegram_id == telegram_id).first()

    @classmethod
    def update_last_checked(cls, telegram_id: int):
        """Обновляет поле last_checked на текущую дату и время."""
        with DatabaseSession() as db:
            user = db.query(cls).filter(cls.telegram_id == telegram_id).first()
            if user:
                user.last_checked = datetime.now().strftime("%A, %Y-%m-%d %H:%M:%S")
                db.commit()
                return user.last_checked
            return None

    @classmethod
    def check_user(cls, telegram_id: int):
        """Возвращает дату последней активности пользователя."""
        with DatabaseSession() as db:
            user = db.query(cls).filter(cls.telegram_id == telegram_id).first()
            return user.last_checked if user else None

    @classmethod
    def to_csv(cls, file_path: str):
        """Экспорт пользователей в CSV с разделителем табуляция."""
        with DatabaseSession() as db:
            users = db.query(cls).all()
            with open(file_path, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file, delimiter="\t")
                writer.writerow(["id", "name", "full_name", "username", "telegram_id", "last_checked"])  # Заголовки
                for user in users:
                    writer.writerow([user.id, user.name, user.full_name, user.username, user.telegram_id, user.last_checked])

    @classmethod
    def from_csv(cls, file_path: str):
        """Импорт пользователей из CSV с разделителем табуляция."""
        with DatabaseSession() as db:
            with open(file_path, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file, delimiter="\t")
                for row in reader:
                    user = cls(
                        #id=int(row["id"]),
                        name=row["name"],
                        full_name=row["full_name"],
                        username=row["username"],
                        telegram_id=int(row["telegram_id"]) if row["telegram_id"] else None,
                        last_checked=row["last_checked"] if row["last_checked"] != 'None' else None
                    )
                    db.add(user)
                db.commit()
