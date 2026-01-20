import streamlit as st
import requests

API_URL = "http://localhost:5000"

st.set_page_config(page_title="Movie Chatbot", page_icon="🎬")
st.title("🎬 Movie Recommendation Chatbot")

# Session state
if "token" not in st.session_state:
    st.session_state.token = None

if "page" not in st.session_state:
    st.session_state.page = "login"

if st.session_state.token:
    choice = st.sidebar.radio("Menu", ["Chat", "Logout"])
else:
    choice = st.sidebar.radio("Menu", ["Login", "Register"])

if choice == "Register":
    st.subheader("📝 Register")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        res = requests.post(
            f"{API_URL}/register",
            json={"username": username, "password": password}
        )

        if res.status_code == 200:
            st.success("Registered successfully! Please login.")
        else:
            st.error(res.json().get("error", "Registration failed"))

elif choice == "Login":
    st.subheader("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        res = requests.post(
            f"{API_URL}/login",
            json={"username": username, "password": password}
        )

        if res.status_code == 200:
            st.session_state.token = res.json()["token"]
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid username or password")

elif choice == "Chat":
    st.subheader("💬 Ask about movies")

    msg = st.text_input("Type your message")

    if msg:
        res = requests.post(
            f"{API_URL}/chat",
            headers={
                "Authorization": f"Bearer {st.session_state.token}"
            },
            json={"message": msg}
        )

        if res.status_code == 200:
            data = res.json()

            st.subheader("🎥 Recommendations")
            for m in data["movies"]:
                st.write("•", m)

            # st.subheader("Remembered Preferences")
            # for p in data["memory"]:
            #     st.write("•", p)
        else:
            st.error("Session expired. Please login again.")

elif choice == "Logout":
    st.session_state.token = None
    st.success("Logged out")
    st.rerun()
