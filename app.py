import pandas as pd
import streamlit as st

from src.prepare_cassandra import prepare_cassandra

st.title("Foodssy")
st.subheader("Available meals")
session = prepare_cassandra()

meals = session.execute("SELECT * FROM meal_by_id;")
meals_df = pd.DataFrame(meals, columns=["meal_id", "meal_type", "provider", "pickup_time"])
st.table(meals_df)
