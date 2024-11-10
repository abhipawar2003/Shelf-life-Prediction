import streamlit as st
from database import register, login
from model import extrapolate_data, predict_shelf_life
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
from io import BytesIO
import base64
import streamlit.components.v1 as components

def load_css(file_name="styles.css"):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def load_custom_css(file_name="style_welcome.css"):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Custom Back Button using Streamlit and CSS styling
def custom_back_button():
    if st.button("🔙 Back", key="back_button"):
        st.session_state['action'] = None
        st.rerun()


def create_pdf_report(data, extrapolated_data, plot_path, study_type):
    pdf = PDF()
    pdf.add_page()

    # Title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "Stability Study Extrapolated Data Report", ln=True, align="C")
    
    # Introduction
    pdf.set_font("Arial", "", 12)
    pdf.ln(10)
    pdf.multi_cell(0, 10, f"This report presents the extrapolated data for the '{study_type}' stability study. "
                           "The objective of this study is to evaluate the stability profile of the drug over an extended period, "
                           "providing insights into shelf-life predictions and storage recommendations.")

    # Original Data Section
    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, "1. Original Data (0-6 months)", ln=True)
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0, 10, "The following table lists the observed dissolution percentages over the first six months. "
                           "This data serves as the basis for extrapolating the drug's stability profile.")

    # Table for Original Data
    pdf.set_font("Arial", "B", 10)
    pdf.cell(40, 10, "Time (Months)", 1, 0, "C")
    pdf.cell(60, 10, "Dissolution (%)", 1, 1, "C")
    
    pdf.set_font("Arial", "", 10)
    for i, row in data.iterrows():
        pdf.cell(40, 10, str(row['time_months']), 1, 0, "C")
        pdf.cell(60, 10, f"{row['dissolution_%']:.2f}", 1, 1, "C")

    # Extrapolated Data Section
    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, "2. Extrapolated Data (7-24 months)", ln=True)
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0, 10, "Using linear regression, we have extrapolated the stability profile up to 24 months. "
                           "This predictive model is based on the initial six-month data, allowing us to estimate the dissolution "
                           "trend over a longer period. The extrapolated dissolution percentages are shown below.")

    # Table for Extrapolated Data
    pdf.set_font("Arial", "B", 10)
    pdf.cell(40, 10, "Time (Months)", 1, 0, "C")
    pdf.cell(60, 10, "Predicted Dissolution (%)", 1, 1, "C")
    
    pdf.set_font("Arial", "", 10)
    for i, row in extrapolated_data.iterrows():
        pdf.cell(40, 10, str(row['time_months']), 1, 0, "C")
        pdf.cell(60, 10, f"{row['predicted_dissolution']:.2f}", 1, 1, "C")

    # Plot Image
    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, "3. Stability Profile Plot", ln=True)
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0, 10, "The following plot visualizes the observed and extrapolated dissolution data. "
                           "The red dashed line represents the dissolution limit, providing a reference for acceptable stability levels.")
    pdf.image(plot_path, x=10, y=pdf.get_y() + 10, w=180)

    # Conclusion Section
    pdf.ln(100)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, "4. Conclusion", ln=True)
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0, 10, "Based on the extrapolated data, the drug demonstrates a stable dissolution profile over the predicted period. "
                           "These results support the estimated shelf life under the specified storage conditions for the selected study type. "
                           "Further real-time studies are recommended to confirm these findings over an extended period.")

    # Save PDF content to a BytesIO buffer
    buffer = BytesIO()
    buffer.write(pdf.output(dest='S').encode('latin1'))
    buffer.seek(0)

    return buffer


class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "Shelf Life Prediction Report", ln=True, align="C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

def create_shelf_life_pdf(data, study_type, threshold, shelf_life):
    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Introduction Section
    pdf.set_font("Arial", "", 11)
    pdf.ln(5)
    pdf.multi_cell(0, 8, f"This report presents the predicted shelf life for the '{study_type}' stability study. "
                           f"The threshold value for dissolution percentage is set at {threshold}%. "
                           "The study aims to predict the estimated shelf life of the drug based on the observed data.")

    # Section 1: Original Data Table
    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "1. Original Data (0-6 months)", ln=True)
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0, 8, "The following table shows the observed dissolution percentages over the first six months, "
                           "providing a basis for the stability profile analysis.")

    # Table Headers
    pdf.set_font("Arial", "B", 10)
    pdf.cell(50, 8, "Time (Months)", 1, 0, "C")
    pdf.cell(50, 8, "Dissolution (%)", 1, 1, "C")

    # Table Rows
    pdf.set_font("Arial", "", 10)
    for i, row in data.iterrows():
        pdf.cell(50, 8, str(row['time_months']), 1, 0, "C")
        pdf.cell(50, 8, f"{row['dissolution_%']:.2f}", 1, 1, "C")

    # Section 2: Shelf Life Prediction
    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "2. Shelf Life Prediction", ln=True)
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0, 8, f"Based on the analysis, the predicted shelf life of the drug is approximately {shelf_life} months. "
                           f"This prediction assumes that the dissolution percentage remains above {threshold}%, "
                           "indicating the drug's stability under the given conditions.")

    # Section 3: Conclusion
    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "3. Conclusion", ln=True)
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0, 8, "The predicted shelf life indicates that the drug is expected to remain stable for the specified period "
                           "under the given storage conditions. However, further real-time stability studies are recommended to confirm "
                           "these findings over an extended duration.")

    # Save PDF to BytesIO buffer
    buffer = BytesIO()
    buffer.write(pdf.output(dest='S').encode('latin1'))
    buffer.seek(0)

    return buffer




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
            result = register(name, username, password)
            if result == "Username already exists.":
                st.error(result)  # Display error message on Streamlit
            else:
                st.success(result)

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

    load_custom_css()

    # Wrap the Welcome Page in a div with class 'welcome-page'
    st.markdown('<div class="welcome-page">', unsafe_allow_html=True)
    
    # Welcome banner and content
    st.markdown('<div class="welcome-banner">Welcome to the Stability Study Analysis Platform!</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="center-content">', unsafe_allow_html=True)
    st.write("This platform allows you to analyze stability study data, predict shelf life, and generate professional reports with ease.")
    st.write("Choose an action below to get started.")

    # Styled buttons
    if st.button("📊 Extrapolate Data"):
        st.session_state['action'] = 'extrapolate'
        st.rerun()

    if st.button("📅 Predict Shelf Life"):
        st.session_state['action'] = 'predict'
        st.rerun()

    if st.button("🔐 Logout"):
        st.session_state.clear()
        st.rerun()

    # End centered content
    st.markdown('</div>', unsafe_allow_html=True)



def plot_simple_graph(data, extrapolated_data):
    plt.figure(figsize=(10, 6))

    # Plot original data
    plt.plot(data['time_months'], data['dissolution_%'], 'o-', color="royalblue", label="Original Data", markersize=6, linewidth=2)

    # Plot extrapolated data
    plt.plot(extrapolated_data['time_months'], extrapolated_data['predicted_dissolution'], 'o--', color="darkorange", label="Extrapolated Data", markersize=6, linewidth=2)

    # Highlight the dissolution limit line at 75%
    plt.axhline(y=75, color='red', linestyle='--', linewidth=1.5, label="Dissolution Limit (75%)")

    # Labels and title
    plt.xlabel('Time (Months)', fontsize=12)
    plt.ylabel('Dissolution %', fontsize=12)
    plt.title('Stability Study - Simple Extrapolation Plot', fontsize=14)

    # Gridlines for readability
    plt.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.7)

    # Add legend
    plt.legend(loc='best')

    # Display the plot in Streamlit
    st.pyplot(plt)
    plt.close()



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
            st.write("**Data Preview:**", data.head())  # Display preview attractively

            # Filter first 6 months of data based on the selected study type
            filtered_data = data[(data['study_type'] == study_type) & (data['time_months'] <= 6)]

            # Check if the correct temperature is used for the study type
            if study_type == "Accelerated" and (filtered_data['temperature'] != 40).any():
                st.error("For Accelerated studies, the temperature must be 40°C.")
            elif study_type == "Real Time" and (filtered_data['temperature'] != 30).any():
                st.error("For Real Time studies, the temperature must be 30°C.")
            elif filtered_data.empty:
                st.error("The uploaded file does not contain 6 months of data for the selected study type.")
            else:
                if st.button("Extrapolate"):
                    # Extrapolate data using Linear Regression
                    extrapolated_data, plot_path = extrapolate_data(filtered_data)

                    # Display extrapolated data in a visually distinct box
                    st.markdown("### 📈 Extrapolated Data (7 to 24 months):")
                    with st.expander(f"Extrapolated Data for {study_type}", expanded=True):
                        st.dataframe(extrapolated_data)

                    plot_simple_graph(filtered_data,extrapolated_data)
                    pdf_buffer = create_pdf_report(filtered_data, extrapolated_data, plot_path,study_type)

                    # Convert the PDF to base64
                    base64_pdf = base64.b64encode(pdf_buffer.getvalue()).decode('utf-8')

                            # display pdf
                    # st.markdown("#### Report Preview:")
                    # st.markdown(
                    #     f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="500" type="application/pdf"></iframe>',
                    #     unsafe_allow_html=True,
                    # )
                    st.markdown("#### Report Preview:")

                    # Use Streamlit's HTML component to embed the PDF
                    components.html(
                        f"""
                        <iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="500" style="border: none;"></iframe>
                        """,
                        height=500,
                    )
                    st.download_button(
                        label="Download Report as PDF",
                        data=pdf_buffer,
                        file_name="extrapolated_data_report.pdf",
                        mime="application/pdf"
                    )
    custom_back_button()
def predict_page():
    st.title("Predict Shelf Life")

    study_type = st.selectbox("Select the Study Type", ["Select Study Type", "Accelerated", "Real Time"])

    if study_type != "Select Study Type":
        uploaded_file = st.file_uploader("Upload Stability Data", type=["csv"])
        st.warning("**Important:** Your file should contain columns `time_months`, `dissolution_%` or `Assay%`.")

        threshold = st.text_input("Enter the threshold value for the provided data (e.g., 75):")

        if uploaded_file:
            data = pd.read_csv(uploaded_file)
            st.write("**Data Preview:**", data.head())

            filtered_data = data[(data['study_type'] == study_type) & (data['time_months'] <= 6)]

            if study_type == "Accelerated" and (filtered_data['temperature'] != 40).any():
                st.error("For Accelerated studies, the temperature must be 40°C.")
            elif study_type == "Real Time" and (filtered_data['temperature'] != 30).any():
                st.error("For Real Time studies, the temperature must be 30°C.")
            elif filtered_data.empty:
                st.error("The uploaded file does not contain 6 months of data for the selected study type or the study type does not match.")
            else:
                if threshold:
                    try:
                        threshold_value = float(threshold)

                        if st.button("Predict Shelf Life"):
                            extrapolated_data, plot_path = extrapolate_data(filtered_data)
                            shelf_life = predict_shelf_life(extrapolated_data, threshold_value)

                            st.markdown(f"### 🕒 Predicted Shelf Life: **{shelf_life} months**")
                            st.success("Shelf life prediction complete!")

                            # Generate and display download button for PDF report
                            pdf_buffer = create_shelf_life_pdf(filtered_data,study_type, threshold_value, shelf_life)

                            # Convert the PDF to base64
                            base64_pdf = base64.b64encode(pdf_buffer.getvalue()).decode('utf-8')

                            # display pdf
                            # st.markdown("#### Report Preview:")
                            # st.markdown(
                            #     f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="500" type="application/pdf"></iframe>',
                            #     unsafe_allow_html=True,
                            # )
                            st.markdown("#### Report Preview:")

                            # Use Streamlit's HTML component to embed the PDF
                            components.html(
                            f"""
                                <iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="500" style="border: none;"></iframe>
                                """,
                                height=500,
                            )
                            st.download_button(
                                label="Download Shelf Life Report as PDF",
                                data=pdf_buffer,
                                file_name="shelf_life_prediction_report.pdf",
                                mime="application/pdf"
                            )

                    except ValueError:
                        st.error("Please enter a valid numerical threshold.")
                else:
                    st.error("Please enter a threshold value.")

    custom_back_button()


if __name__ == "__main__":

    # Rest of the code logic
    if 'logged_in' in st.session_state and st.session_state['logged_in']:
        if 'action' in st.session_state and st.session_state['action'] == 'extrapolate':
            extrapolate_page()
        elif 'action' in st.session_state and st.session_state['action'] == 'predict':
            predict_page()
        else:
            welcome_page()
    else:
        main()

