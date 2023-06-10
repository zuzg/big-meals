import streamlit as st
import random 
from src.query import truncate_all

from src.query import QueryReservation, QueryMeal, truncate_all
from src.prepare_cassandra import fill_meals
from src.perform_reserve_cancel import perform_reservation, perform_cancellation


def prepare_test_meals(session, n: int) -> None:
    query_meal = QueryMeal(session)
    fill_meals(query_meal, n)

    meals = session.execute(
        """
        SELECT meal_id
        FROM meal_by_id;
        """
    )
    meal_ids = [str(row.meal_id) for row in meals]
    return meal_ids


def perform_test1(session, number_actions: int = 10, repeat: int = 3) -> None:
    
    query_reservation = QueryReservation(session)
    meal_ids = prepare_test_meals(session, 5)

    for n in range(number_actions):
        meal = random.choice(meal_ids)
        if random.random() <= 0.7:
            func = perform_reservation
        else:
            func = perform_cancellation
        for r in range(repeat):
            func(query_reservation, meal, f"test_1_client")

    st.info(f"Test 1 performed successfully.")


def perform_test2(session, number_clients: int = 2, number_actions: int = 100):

    query_reservation = QueryReservation(session)
    meal_ids = prepare_test_meals(session, 50)

    collisions = 0
    wrong_cancel = 0
    for _ in range(number_actions):
        for i in range(number_clients):
            if random.random() <= 0.5:
                collisions += perform_reservation(query_reservation, random.choice(meal_ids), f"test_2_client_{i+1}", test_mode=True)
            else:
                wrong_cancel += perform_cancellation(query_reservation, random.choice(meal_ids), f"test_2_client_{i+1}", test_mode=True)
    st.info(f"Test 2 performed successfully.  \nRecorded {collisions} reservation attempt(s) for already existing reservation and {wrong_cancel} attampt(s) for invalid cancellation(s).")


def perform_test3(session) -> None:

    query_reservation = QueryReservation(session)
    meal_ids = prepare_test_meals(session, 100)

    for meal in meal_ids:
        perform_reservation(query_reservation, meal, f"test_3_client_{random.choice([1, 2])}", test_mode=True)

    st.info(f"Test 3 performed successfully.")

def perform_test4(session, N: int = 31) -> None:

    query_reservation = QueryReservation(session)
    meal_id = prepare_test_meals(session, 1)[0]

    for n in range(N):
        if n % 2 == 0:
            perform_reservation(query_reservation, meal_id, f"test_4_client")
        else:
            perform_cancellation(query_reservation, meal_id, f"test_4_client")

    st.info(f"Test 4 performed successfully.")


def stress_test1() -> None:
    st.subheader("1. The client makes the same request very quickly.")
    execution_button = st.button("Execute Test 1")
    if execution_button:

        session = st.session_state["session"]
        truncate_all(session)
        perform_test1(session)


def stress_test2() -> None:
    st.subheader("2. Two or more clients make the possible requests randomly.")
    execution_button = st.button("Execute Test 2")
    if execution_button:
        session = st.session_state["session"]
        truncate_all(session)
        perform_test2(session)


def stress_test3() -> None:
    st.subheader("2. Immediate occupancy of all seats/reservations on 2 clients.")
    execution_button = st.button("Execute Test 3")
    if execution_button:
        session = st.session_state["session"]
        truncate_all(session)
        perform_test3(session)


def stress_test4() -> None:
    st.subheader("3. Constant cancellations and seat occupancy.")
    execution_button = st.button("Execute Test 4")
    if execution_button:
        session = st.session_state["session"]
        truncate_all(session)
        perform_test4(session)
