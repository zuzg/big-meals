import streamlit as st

from src.prepare_cassandra import prepare_cassandra
from src.app_pages import global_page, user_page


def main() -> None:
    session = None
    try:
        session = prepare_cassandra()
    except:
        st.error("Couldn't connect to the database.")

    if session:
        st.set_page_config(
            page_title="BIG meals",
            page_icon="🥗",
        )
        if "session" not in st.session_state:
            st.session_state["session"] = session
        st.sidebar.title(f"🥗 BIG meals")
        pages = {
            "Global": global_page,
            "User": user_page,
        }
        name = st.sidebar.radio('Choose page', pages.keys(), index=0)
        pages[name]()


if __name__ == "__main__":
    main()
