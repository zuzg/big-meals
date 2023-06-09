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
            WHERE meal_id = ?
            ALLOW FILTERING
            """
        )
        bound = prepared.bind((uuid.UUID(meal_id),))

        with RESERVATION_LOCK:
            meal_info = session.execute(bound)[0]
            row = qr.insert(uuid.UUID(meal_id), client_name, meal_info.provider, meal_info.pickup_time)[0]

        if not row.applied:
            if test_mode:
                return 1
            st.error("The meal has been already reserved!")
        else:
            if test_mode:
                return 0
            st.success("The meal has been booked successfully!", icon="✅")
    except:
        st.error("Invalid MEAL ID!")


def perform_cancellation(qr: QueryReservation, meal_id: str, client_name: str, test_mode:bool=False) -> None:
    global CANCELLATION_LOCK 
    # TODO: verify the user who cancells a reservation
    try:
        qr.cancel(uuid.UUID(meal_id), client_name)
    except:
        st.error("Invalid MEAL ID!")