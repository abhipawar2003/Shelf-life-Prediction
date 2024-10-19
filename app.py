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
            if register(name, username, password):
                st.success("Registered successfully!")
            else:
                st.error("Username already exists.")

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

    # Dropdown to select the study type before file upload
    study_type = st.selectbox("Select the Study Type", ["Select Study Type", "Accelerated", "Real Time"])

    if study_type != "Select Study Type":
        # File uploader for CSV
        uploaded_file = st.file_uploader("Upload Stability Data", type=["csv"])

        if uploaded_file:
            # Read the CSV file
            data = pd.read_csv(uploaded_file)
            st.write("Data Preview:", data.head())

            # Filter first 6 months of data based on the selected study type
            filtered_data = data[(data['study_type'] == study_type) & (data['time_months'] <= 6)]

            if filtered_data.empty:
                st.error("The uploaded file does not contain 6 months of data for the selected study type.")
            else:
                if st.button("Extrapolate"):
                    # Extrapolate data using Linear Regression
                    extrapolated_data, plot_path = extrapolate_data(filtered_data)

                    # Display extrapolated data as a table
                    st.write(f"Extrapolated Data for {study_type} (7 to 24 months):", extrapolated_data)

                    # Show the plot of extrapolated data
                    st.image(plot_path)

    # Back button
    if st.button("Back"):
        st.session_state['action'] = None
        st.rerun()

def predict_page():
    st.title("Predict Shelf Life")

    # Dropdown to select the study type before file upload
    study_type = st.selectbox("Select the Study Type", ["Select Study Type", "Accelerated", "Real Time"])

    if study_type != "Select Study Type":
        # File uploader for CSV
        uploaded_file = st.file_uploader("Upload Stability Data", type=["csv"])
        st.warning("**Important:** Your file should contain the following columns: `time_month`, `dissolution% ` or `Assay%`.")



        if uploaded_file:
            # Read the CSV file
            data = pd.read_csv(uploaded_file)
            st.write("Data Preview:", data.head())

            # Filter first 6 months of data based on the selected study type
            filtered_data = data[(data['study_type'] == study_type) & (data['time_months'] <= 6)]

            if filtered_data.empty:
                st.error("The uploaded file does not contain 6 months of data for the selected study type or the study type does not match.")
            else:
        
                if ((filtered_data["study_type"].str.lower().str.strip() == "accelerated") & (filtered_data["temperature"] == 40)).any() or \
                    ((filtered_data["study_type"].str.lower().str.strip() == "realtime") & (filtered_data["temperature"] == 30)).any():
    # Your logic here


                    if st.button("Predict Shelf Life"):
                        # Extrapolate the data using Linear Regression
                        extrapolated_data, plot_path = extrapolate_data(filtered_data)

                        # Predict the shelf life using Quadratic Regression
                        shelf_life = predict_shelf_life(extrapolated_data)
                        st.write(f"Predicted Shelf Life for {study_type}: {shelf_life} months")

                else:
                    st.error("temperature does not match with study type")
                    
    if st.button("Back"):
        st.session_state['action'] = None
        st.rerun()


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
