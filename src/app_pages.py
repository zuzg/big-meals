import uuid
import pandas as pd
import streamlit as st

from src.query import QueryReservation


def reservation(qr: QueryReservation) -> None:
    st.subheader("Reserve a meal")
    meal_id = st.text_input("Meal identifier")
    try:
        qr.insert(uuid.UUID(meal_id), "Agatka")
    except:
        st.write("Enter a valid id")


def global_page() -> None:
    st.title("Global state of reservations")
    st.subheader("Available meals")
    session = st.session_state["session"]

    meals = session.execute("SELECT * FROM meal_by_id;")
    meals_df = pd.DataFrame(
        meals,
        columns=["meal_id", "is_available", "meal_type", "pickup_time", "provider"],
    )
    st.dataframe(meals_df)

    qr = QueryReservation(session)
    reservation(qr)

    st.subheader("Reserved meals")
    reservations = session.execute("SELECT * FROM reservation_by_meal;")
    reservation_df = pd.DataFrame(
        reservations, columns=["meal_id", "client_name", "timestamp"]
    )
    st.dataframe(reservation_df)


def user_page() -> None:
    st.title("Foodsy")
    st.subheader("Choose a meal to reserve")
    session = st.session_state["session"]
    meals = session.execute("SELECT * FROM meal_by_id;")
    meals_df = pd.DataFrame(
        meals,
        columns=["meal_id", "is_available", "meal_type", "pickup_time", "provider"],
    )
    st.dataframe(meals_df)
