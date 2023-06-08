import streamlit as st

from src.prepare_cassandra import prepare_cassandra
from src.app_pages import global_page, user_page, stress_page

def main() -> None:
    session = None
    try:
        session = prepare_cassandra()
    except:
        st.error("Couldn't connect to the database.")

    if session:
        st.set_page_config(
            page_title="Foodsy",
            page_icon="🥗",
            layout="wide",
        )
        if "session" not in st.session_state:
            st.session_state["session"] = session
        st.sidebar.title(f"🥗 Foodsy")
        pages = {
            "Admin": global_page,
            "User Zuza": user_page,
            "User Agata": user_page,
            "Stress tests": stress_page,
        }
        user_names = {
            "User Zuza": "Zuza",
            "User Agata": "Agata"
        }

        name = st.sidebar.radio("CHOOSE A PAGE", pages.keys())
        if name.startswith("User"):
            pages[name](user_names[name])
        else:
            pages[name]()


if __name__ == "__main__":
    main()
