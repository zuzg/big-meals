import uuid
import pandas as pd
import streamlit as st

from src.query import QueryReservation, QueryMeal, truncate_all
from src.prepare_cassandra import fill_meals
from src.perform_reserve_cancel import perform_reservation, perform_cancellation
from src.stress_tests import stress_test1, stress_test2, stress_test3, stress_test4


def reservation(qr: QueryReservation, client_name: str) -> None:
    st.subheader("Reserve a meal")
    col1, col2 = st.columns([2, 1])
    with col1: 
        meal_id = st.text_input("Enter MEAL ID:", "MEAL ID", key="res", label_visibility="collapsed")
    with col2:
        reserve_button = st.button("Reserve")

    if reserve_button:
        perform_reservation(qr, meal_id, client_name)


def cancellation(qr: QueryReservation, client_name: str) -> None:
    st.subheader("Cancel reservation")
    col1, col2 = st.columns([2, 1])
    with col1: 
        meal_id = st.text_input("Enter MEAL ID:", "MEAL ID", key="cancel", label_visibility="collapsed")
    with col2:
        cancel_button = st.button("Confirm")
    if cancel_button:
        perform_cancellation(qr, meal_id, client_name)


def get_reservations(user_view: bool, client_name: str = "") -> None:
    session = st.session_state["session"]
    if user_view:
        prepared = session.prepare(
            """
            SELECT meal_id, provider, pickup_time, reservation_timestamp 
            FROM reservations
            WHERE client_name = ?
            ALLOW FILTERING
            """
        )
        bound = prepared.bind((client_name,))
        reservations = session.execute(bound)
        columns = ["MEAL ID", "PROVIDER", "PICKUP TIME", "RESERVED AT"]
    else:
        reservations = session.execute(
            """
            SELECT meal_id, client_name, reservation_timestamp 
            FROM reservations;
            """
        )
        columns = ["meal_id", "client_name", "timestamp"]

    reservation_df = pd.DataFrame(reservations, columns=columns)
    st.dataframe(reservation_df, use_container_width=True)


def global_page() -> None:
    st.title("Global state of reservations")
    session = st.session_state["session"]
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("List of meals")

        meals = session.execute("SELECT * FROM meal_by_id;")
        meals_df = pd.DataFrame(
            meals,
            columns=["MEAL ID", "AVAILABLE", "TYPE", "PICKUP TIME", "PROVIDER"],
        )
        st.dataframe(meals_df)
        st.subheader("Reserved meals")
        get_reservations(user_view=False)

    with col2:
        st.subheader("Manage database")
        with st.form("Add meals"):
            n = st.number_input(
                "Number of meals to insert", min_value=1, max_value=100, value=1, step=1
            )
            if st.form_submit_button("Add meals"):
                try:
                    query = QueryMeal(session)
                    fill_meals(query, n)
                    st.info(f"{n} new meals(s) has(ve) been added to the database.")
                except Exception as e:
                    st.error(f"Cannot fill the database with {n} new meals. {e}")
        if st.button("Truncate all tables"):
            truncate_all(session)


def user_page(client_name:str) -> None:
    session = st.session_state["session"]
    qr = QueryReservation(session)
    st.title(f"Hi {client_name},")
    st.markdown("### *save some food with Foodsy!*")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("List of meals")
        meals = session.execute("SELECT * FROM meal_by_id;")
        meals_df = pd.DataFrame(
            meals,
            columns=["MEAL ID", "AVAILABLE", "TYPE", "PICKUP TIME", "PROVIDER"],
        )
        st.dataframe(meals_df)
        

    with col2:
        st.subheader("Your reservations")
        get_reservations(user_view=True, client_name=client_name)
        reservation(qr, client_name)
        cancellation(qr, client_name)


def stress_page() -> None:
    st.title("Stress tests")
    st.markdown("*Note: Each test truncates present data at the beginning as it creates new data.*")
    stress_test1()
    stress_test2()
    stress_test3()
    stress_test4()
