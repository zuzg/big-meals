import streamlit as st
import random 
from src.query import truncate_all

from src.query import QueryReservation, QueryMeal, truncate_all
from src.prepare_cassandra import fill_meals
from src.perform_reserve_cancel import perform_reservation



def perform_test1(session, number_clients: int = 2, number_actions: int = 100):

    n_rows = 50
    query_meal = QueryMeal(session)
    fill_meals(query_meal, n_rows)

    query_reservation = QueryReservation(session)

    meals = session.execute(
        """
        SELECT meal_id
        FROM meal_by_id;
        """
    )
    meal_ids = [str(row.meal_id) for row in meals]


    collisions = 0
    # TODO: cancellation verification
    wrong_cancel = 0
    for _ in range(number_actions):
        for i in range(number_clients):
            if random.random() <= 0.5:
                collisions += perform_reservation(query_reservation, random.choice(meal_ids), f"client_{i+1}", test_mode=True)
            else:
                wrong_cancel += 0
    st.info(f"Test 1 performed successfully.  \nRecorded {collisions} attempts for already existing reservation and {wrong_cancel} invalid cancellations.")

def stress_test1() -> None:
    st.subheader("1. Two or more clients make the possible requests randomly.")
    execution_button = st.button("Execute")
    if execution_button:

        session = st.session_state["session"]
        truncate_all(session)

        perform_test1(session)


def stress_test2() -> None:
    st.subheader("2. Immediate occupancy of all seats/reservations on 2 clients.")
    st.write("TODO")

def stress_test3() -> None:
    st.subheader("3. Constant cancellations and seat occupancy.")
    st.write("TODO")
