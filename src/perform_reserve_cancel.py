import uuid
import pandas as pd
import streamlit as st
import threading

from src.query import QueryReservation

RESERVATION_LOCK = threading.Lock()
CANCELLATION_LOCK = threading.Lock()

def perform_reservation(qr: QueryReservation, meal_id: str, client_name, test_mode:bool=False) -> None:
    global RESERVATION_LOCK
    try:
        session = st.session_state["session"]
        prepared = session.prepare(
            """
            SELECT meal_id, provider, pickup_time
            FROM meal_by_id
            WHERE meal_id = ? and available = true
            ALLOW FILTERING
            """
        )
        bound = prepared.bind((uuid.UUID(meal_id),))

        with RESERVATION_LOCK:
            meal_info = session.execute(bound)
            if not meal_info.one():
                if test_mode:
                    return 1
                st.error("The meal has been already reserved!")
                return None
            meal_info = meal_info.one()
            qr.insert(uuid.UUID(meal_id), client_name, meal_info.provider, meal_info.pickup_time)

            if test_mode:
                return 0
            st.success("The meal has been booked successfully!", icon="✅")
    except Exception as e:
        st.error(f"{e}")


def perform_cancellation(qr: QueryReservation, meal_id: str, client_name: str, test_mode:bool=False) -> None:
    global CANCELLATION_LOCK 
    try:
        session = st.session_state["session"]
        prepared = session.prepare(
                """
                SELECT meal_id, client_name
                FROM reservations
                WHERE meal_id = ? and client_name = ?
                """
            )
        bound = prepared.bind((uuid.UUID(meal_id), client_name))

        with CANCELLATION_LOCK:
            res_info = session.execute(bound)

            if not res_info.one():
                if test_mode:
                    return 1
                st.error("No such MEAL ID found in your reservations!")
                return None

            qr.cancel(uuid.UUID(meal_id), client_name)
            if test_mode:
                return 0
            st.success("The meal has been cancelled successfully!", icon="✅")

    except:
        st.error(f"Invalid MEAL ID!")