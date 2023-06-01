import pandas as pd
import streamlit as st
from cassandra.cluster import Cluster


def set_up_cluster():
    cluster = Cluster(["127.0.0.1"], port=9042)
    session = cluster.connect()
    session.execute(
        """CREATE KEYSPACE IF NOT EXISTS store WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : '1' };"""
    )
    session.execute(
        """
    CREATE TABLE IF NOT EXISTS store.shopping_cart (
    userid text PRIMARY KEY,
    item_count int,
    last_update_timestamp timestamp
    );
    """
    )
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

    return session


st.title("Big data project")
st.subheader("Shopping cart")
session = set_up_cluster()
users = session.execute(
    """
    SELECT * FROM store.shopping_cart;
    """
)

user_df = pd.DataFrame(users, columns=["user_id", "item_count", "timestamp"])
st.table(user_df)
