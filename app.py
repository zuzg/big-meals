import pandas as pd
import streamlit as st

from src.prepare_cassandra import prepare_cassandra


def add_rows(session):
    session.execute(
        """
    INSERT INTO store.shopping_cart
    (userid, item_count, last_update_timestamp)
    VALUES ('9876', 2, toTimeStamp(now()));
    """
    )
    session.execute(
        """
    INSERT INTO store.shopping_cart
    (userid, item_count, last_update_timestamp)
    VALUES ('1234', 5, toTimeStamp(now()));
    """
    )


st.title("Big data project")
st.subheader("Shopping cart")
session = prepare_cassandra()
add_rows(session)

users = session.execute(
    """
    SELECT * FROM store.shopping_cart;
    """
)

user_df = pd.DataFrame(users, columns=["user_id", "item_count", "timestamp"])
st.table(user_df)
