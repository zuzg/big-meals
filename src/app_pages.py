import uuid
import pandas as pd
import streamlit as st

from src.query import QueryReservation, QueryMeal, truncate_all
from src.prepare_cassandra import fill_meals
from src.stress_tests import stress_test1, stress_test2, stress_test3


def reservation(qr: QueryReservation, client_name) -> None:
    st.subheader("Reserve a meal")
    # st.markdown("Enter MEAL ID:")
    col1, col2 = st.columns([2, 1])
    with col1: 
        meal_id = st.text_input("Enter MEAL ID:", "MEAL ID", key="res", label_visibility="collapsed")
    with col2:
        reserve_button = st.button("Reserve")

    if reserve_button:
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
            meal_info = session.execute(bound)[0]

            row = qr.insert(uuid.UUID(meal_id), client_name, meal_info.provider, meal_info.pickup_time)[0]
            if not row.applied:
                st.markdown(":red[**THE MEAL HAS BEEN ALREADY RESERVED!**]")
        except:
            st.markdown(":red[**INVALID MEAL ID!**]")


def cancellation(qr: QueryReservation) -> None:
    st.subheader("Cancel reservation")
    # st.markdown("Enter MEAL ID:")
    col1, col2 = st.columns([2, 1])
    with col1: 
        meal_id = st.text_input("Enter MEAL ID:", "MEAL ID", key="cancel", label_visibility="collapsed")
    with col2:
        cancel_button = st.button("Confirm")
    if cancel_button:
        try:
            qr.cancel(uuid.UUID(meal_id))
        except:
            st.markdown(":red[**INVALID MEAL ID!**]")


def get_reservations(user_view: bool, client_name: str = "") -> None:
    session = st.session_state["session"]
    if user_view:
        # TODO join with meals (or new table by_client?)
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
        columns = ["MEAL ID", "PROVIDER", "PICKUP AT", "RESERVED AT"]
    else:
        reservations = session.execute(
            """
            SELECT meal_id, client_name, reservation_timestamp 
            FROM reservations;
            """
        )
        columns = ["meal_id", "client_name", "timestamp"]

    reservation_df = pd.DataFrame(reservations, columns=columns)
    st.dataframe(reservation_df, hide_index=True)


def global_page() -> None:
    st.title("Global state of reservations")
    session = st.session_state["session"]
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("List of meals")

        meals = session.execute("SELECT * FROM meal_by_id;")
        meals_df = pd.DataFrame(
            meals,
            columns=["meal_id", "is_available", "meal_type", "pickup_time", "provider"],
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
                except:
                    st.error(f"Cannot fill the database with {n} new meals.")
        if st.button("Truncate all tables"):
            try:
                truncate_all(session)
                st.info("All tables trunkated.")
            except:
                st.error(f"Cannot truncate tables.")


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
            columns=["MEAL ID", "AVAILABLE", "TYPE", "PICKUP AT", "PROVIDER"],
        )
        st.dataframe(meals_df, hide_index=True)
        

    with col2:
        st.subheader("Your reservations")
        get_reservations(user_view=True, client_name=client_name)
        reservation(qr, client_name)
        cancellation(qr)


def stress_page() -> None:
    st.title("Stress tests")
    stress_test1()
    stress_test2()
    stress_test3()
