from cassandra.cluster import Session, ResultSet
import uuid
import datetime


class QueryMeal:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.prepared_insert = session.prepare(
            "INSERT INTO meal_by_id (meal_id, meal_type, provider, pickup_time) "
            "VALUES (?, ?, ?, ?) IF NOT EXISTS"
        )

    def insert(self, meal_type: str, provider: str, pickup_time: datetime) -> None:
        meal_id = uuid.uuid1()
        bound = self.prepared_insert.bind((meal_id, meal_type, provider, pickup_time))
        self.session.execute(bound)

    def drop(self) -> None:
        query = f"DROP TABLE meal_by_id"
        self.execute(query)
