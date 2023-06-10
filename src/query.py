from cassandra.cluster import Session
import streamlit as st
import uuid
import datetime


class QueryMeal:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.prepared_insert = session.prepare(
            "INSERT INTO meal_by_id (meal_id, meal_type, provider, pickup_time, available) "
            "VALUES (?, ?, ?, ?, ?) IF NOT EXISTS"
        )

    def insert(self, meal_type: str, provider: str, pickup_time: datetime) -> None:
        meal_id = uuid.uuid1()
        bound = self.prepared_insert.bind(
            (meal_id, meal_type, provider, pickup_time, True)
        )
        self.session.execute(bound)

    def drop(self) -> None:
        query = f"DROP TABLE meal_by_id"
        self.session.execute(query)


class QueryReservation:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.prepared_insert = session.prepare(
            "INSERT INTO reservations (meal_id, client_name, provider, pickup_time, reservation_timestamp) "
            "VALUES (?, ?, ?, ?, ?) IF NOT EXISTS"
        )
        self.prepared_delete = session.prepare(
            """
            DELETE
            FROM reservations 
            WHERE meal_id = ? AND client_name = ?
            """
        )
        self.meal_update = self.session.prepare(
            "UPDATE meal_by_id SET available = ? WHERE meal_id = ?"
        )
        self.prepared_res_update = self.session.prepare(
            "UPDATE reservations SET note = ? WHERE meal_id = ? AND client_name = ?"
        )

    def insert(
        self, meal_id: uuid.UUID, client_name: str, provider: str, pickup_time: int
    ) -> list[dict]:
        bound = self.prepared_insert.bind(
            (meal_id, client_name, provider, pickup_time, datetime.datetime.now())
        )
        res = self.session.execute(bound)
        if res[0].applied:
            query = self.meal_update.bind((False, meal_id))
            self.session.execute(query)
        return res

    def cancel(self, meal_id: uuid.UUID, client_name: str):
        bound = self.prepared_delete.bind((meal_id, client_name))
        self.session.execute(bound)

        query = self.meal_update.bind((True, meal_id))
        self.session.execute(query)

    def update_note(self, meal_id: uuid.UUID, client_name: str, text: str):
        bound = self.prepared_res_update.bind((text, meal_id, client_name))
        self.session.execute(bound)

    def drop(self) -> None:
        query = f"DROP TABLE reservations"
        self.session.execute(query)


def truncate_all(session: Session) -> None:
    try:
        tables = ["meal_by_id", "reservations"]
        for table in tables:
            session.execute(f"TRUNCATE {table}")
        st.info("All tables truncated.")
    except:
        st.error(f"Cannot truncate tables.")
