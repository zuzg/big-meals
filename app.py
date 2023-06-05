import pandas as pd
import streamlit as st
import uuid

from src.prepare_cassandra import prepare_cassandra
from src.query import QueryReservation


def reservation(qr: QueryReservation) -> None:
    st.subheader("Reserve a meal")
    meal_id = st.text_input("Meal identifier")
    try:
        qr.insert(uuid.UUID(meal_id), "Agatka")
    except:
        st.write("Enter a valid id")


st.title("Foodssy")
st.subheader("Available meals")
session = prepare_cassandra()

meals = session.execute("SELECT * FROM meal_by_id;")
meals_df = pd.DataFrame(meals, columns=["meal_id", "is_available", "meal_type", "pickup_time", "provider"])
st.dataframe(meals_df)

qr = QueryReservation(session)
reservation(qr)

st.subheader("Reserved meals")
reservations = session.execute("SELECT * FROM reservation_by_meal;")
reservation_df = pd.DataFrame(reservations, columns=["meal_id", "client_name", "timestamp"])
st.dataframe(reservation_df)
