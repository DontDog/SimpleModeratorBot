from sqlalchemy import Column, Integer, String, create_engine
from db.database import Base, DatabaseSession

# Определяем модель для таблицы State
class State(Base):
    __tablename__ = 'state'

    id = Column(Integer, primary_key=True)
    key = Column(String, nullable=False)
    value = Column(String)

    @classmethod
    def set(cls, key: str, value: str):
        """Устанавливает значение для указанного ключа."""
        # Проверяем, существует ли запись с таким ключом
        with DatabaseSession() as db:
            state = cls(key=key, value=value)
            db.add(state)
            db.commit()

    @classmethod
    def get(cls, key: str):
        """Возвращает значение для указанного ключа."""
        with DatabaseSession() as db:
            state = db.query(cls).filter_by(key=key).all()
            return list(map(lambda x: x.value, state)) if state else None

    @classmethod
    def remove(cls, key: str):
        """Удаляет значение для указанного ключа."""
        with DatabaseSession() as db:
            states = db.query(cls).filter_by(key=key).all()
            for state in states:
                db.delete(state)
            db.commit()
