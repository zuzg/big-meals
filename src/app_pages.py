import uuid
import pandas as pd
import streamlit as st

from src.query import QueryReservation, QueryMeal, truncate_all
from src.prepare_cassandra import fill_meals


def reservation(qr: QueryReservation) -> None:
    st.subheader("Reserve a meal")
    meal_id = st.text_input("Meal identifier")
    try:
        qr.insert(uuid.UUID(meal_id), "Agatka")
    except:
        st.write("Enter a valid id")


def global_page() -> None:
    st.title("Global state of reservations")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("Available meals")
        session = st.session_state["session"]

        meals = session.execute("SELECT * FROM meal_by_id;")
        meals_df = pd.DataFrame(
            meals,
            columns=["meal_id", "is_available", "meal_type", "pickup_time", "provider"],
        )
        st.dataframe(meals_df)
        st.subheader("Reserved meals")
        reservations = session.execute("SELECT * FROM reservation_by_meal;")
        reservation_df = pd.DataFrame(
            reservations, columns=["meal_id", "client_name", "timestamp"]
        )
        st.dataframe(reservation_df)

    with col2:
        st.subheader("Manage database")
        with st.form("Add meals"):
            n = st.number_input("Number of meals to insert", min_value=1, max_value=100, value=1, step=1)
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


def user_page() -> None:
    st.title("Foodsy")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Choose a meal to reserve")
        session = st.session_state["session"]
        meals = session.execute("SELECT * FROM meal_by_id;")
        meals_df = pd.DataFrame(
            meals,
            columns=["meal_id", "is_available", "meal_type", "pickup_time", "provider"],
        )
        st.dataframe(meals_df)
        qr = QueryReservation(session)
        reservation(qr)

    with col2:
        st.subheader("Your reservations")
        st.text("TODO")
