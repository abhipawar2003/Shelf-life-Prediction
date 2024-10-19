# # app.py
# import streamlit as st
# from database import register, login

# def main():
#     st.title("User Registration and Login")

#     menu = ["Register", "Login"]
#     choice = st.sidebar.selectbox("Select Action", menu)

#     if choice == "Register":
#         st.subheader("Register")
#         name = st.text_input("Name")
#         username = st.text_input("Username")
#         password = st.text_input("Password", type='password')

#         if st.button("Register"):
#             register(name, username, password)
#             st.success("Registered successfully!")

#     elif choice == "Login":
#         st.subheader("Login")
#         username = st.text_input("Username")
#         password = st.text_input("Password", type='password')

#         if st.button("Login"):
#             if login(username, password):
#                 st.success("Logged in successfully!")
#             else:
#                 st.error("Login failed. Check your username and password.")

# if __name__ == "__main__":
#     main()
# import streamlit as st
# from database import register, login

# def main():
#     st.title("User Registration and Login")

#     menu = ["Register", "Login"]
#     choice = st.sidebar.selectbox("Select Action", menu)

#     if choice == "Register":
#         st.subheader("Register")
#         name = st.text_input("Name")
#         username = st.text_input("Username")
#         password = st.text_input("Password", type='password')

#         if st.button("Register"):
#             register(name, username, password)
#             st.success("Registered successfully!")

#     elif choice == "Login":
#         st.subheader("Login")
#         username = st.text_input("Username", key="login_username")
#         password = st.text_input("Password", type='password', key="login_password")

#         if st.button("Login"):
#             if login(username, password):
#                 st.session_state['username'] = username
#                 st.session_state['logged_in'] = True  # Set logged_in state
#                 st.rerun()  # Refresh to show welcome page
#             else:
#                 st.error("Login failed. Check your username and password.")

# def welcome_page():
#     st.title("Welcome Page")
#     st.write(f"Welcome, {st.session_state['username']}!")
    
#     # Logout button
#     if st.button("Logout"):
#         st.session_state.clear()  # Clear the session state
#         st.rerun()  # Refresh to go back to the login page

# if __name__ == "__main__":
#     # Check if the user is logged in
#     if 'logged_in' in st.session_state and st.session_state['logged_in']:
#         welcome_page()  # Show welcome page
#     else:
#         main()  # Show main registration/login page

import streamlit as st
from database import register, login
from model import extrapolate_data, predict_shelf_life
import pandas as pd

def main():
    st.title("User Registration and Login")

    menu = ["Register", "Login"]
    choice = st.sidebar.selectbox("Select Action", menu)

    if choice == "Register":
        st.subheader("Register")
        name = st.text_input("Name")
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')

        if st.button("Register"):
            register(name, username, password)
            st.success("Registered successfully!")

    elif choice == "Login":
        st.subheader("Login")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type='password', key="login_password")

        if st.button("Login"):
            if login(username, password):
                st.session_state['username'] = username
                st.session_state['logged_in'] = True
                st.rerun()  # Refresh to show welcome page
            else:
                st.error("Login failed. Check your username and password.")

def welcome_page():
    st.title("Welcome Page")
    st.write(f"Welcome, {st.session_state['username']}!")

    if st.button("Extrapolate Data"):
        st.session_state['action'] = 'extrapolate'
        st.rerun()

    if st.button("Predict Shelf Life"):
        st.session_state['action'] = 'predict'
        st.rerun()

    if st.button("Logout"):
        st.session_state.clear()  # Clear session state
        st.rerun()

def extrapolate_page():
    st.title("Extrapolate Data")
    uploaded_file = st.file_uploader("Upload 6 Months Stability Data", type=["csv"])

    if uploaded_file:
        data = pd.read_csv(uploaded_file)
        st.write("Data Preview:", data.head())

        if st.button("Extrapolate"):
            extrapolated_data = extrapolate_data(data)
            st.write("Extrapolated Data:", extrapolated_data)

def predict_page():
    st.title("Predict Shelf Life")
    uploaded_file = st.file_uploader("Upload 6 Months Stability Data", type=["csv"])

    if uploaded_file:
        data = pd.read_csv(uploaded_file)
        st.write("Data Preview:", data.head())

        if st.button("Predict Shelf Life"):
            shelf_life = predict_shelf_life(data)
            st.write(f"Predicted Shelf Life: {shelf_life} months")

if __name__ == "__main__":
    if 'logged_in' in st.session_state and st.session_state['logged_in']:
        if 'action' in st.session_state and st.session_state['action'] == 'extrapolate':
            extrapolate_page()
        elif 'action' in st.session_state and st.session_state['action'] == 'predict':
            predict_page()
        else:
            welcome_page()
    else:
        main()
