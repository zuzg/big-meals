from cassandra.cluster import Session
import uuid
import datetime


class QueryMeal:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.prepared_insert = session.prepare(
            "INSERT INTO meal_by_id (meal_id, meal_type, provider, pickup_time, is_available) "
            "VALUES (?, ?, ?, ?, ?) IF NOT EXISTS"
        )

    def insert(self, meal_type: str, provider: str, pickup_time: datetime) -> None:
        meal_id = uuid.uuid1()
        bound = self.prepared_insert.bind((meal_id, meal_type, provider, pickup_time, True))
        self.session.execute(bound)

    def drop(self) -> None:
        query = f"DROP TABLE meal_by_id"
        self.session.execute(query)


class QueryReservation:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.prepared_insert = session.prepare(
            "INSERT INTO reservations (meal_id, client_name, reservation_timestamp) "
            "VALUES (?, ?, ?) IF NOT EXISTS"
        )
        self.prepared_delete = session.prepare(
            "DELETE FROM reservations WHERE meal_id = ?"
        )
        self.meal_update = self.session.prepare(
            "UPDATE meal_by_id SET is_available = ? WHERE meal_id = ?"
            )

    def insert(
        self,
        meal_id: uuid.UUID,
        client_name: str,
    ) -> None:
        bound = self.prepared_insert.bind((meal_id, client_name, datetime.datetime.now()))
        self.session.execute(bound)
        query = self.meal_update.bind((False, meal_id))
        self.session.execute(query)

    def cancel(self, meal_id: uuid.UUID) -> None:
        bound = self.prepared_delete.bind((meal_id,))
        self.session.execute(bound)
        query = self.meal_update.bind((True, meal_id))
        self.session.execute(query)

    def drop(self) -> None:
        query = f"DROP TABLE reservations"
        self.session.execute(query)


def truncate_all(session: Session) -> None:
    tables = ["meal_by_id", "reservations"]
    for table in tables:
        session.execute(f"TRUNCATE {table}")
