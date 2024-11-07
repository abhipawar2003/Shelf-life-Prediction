# Shelf-Life Prediction and Stability Study Analysis Platform

## Overview
This platform is designed to facilitate stability study data analysis, enabling users to extrapolate dissolution data and predict the shelf life of drugs. Users can upload their stability data and use advanced machine learning models for predictive analysis, generate detailed PDF reports, and visualize the stability profile.

## Features
- **User Registration and Login**: Secure user authentication for personalized sessions.
- **Data Extrapolation**: Upload CSV data to extrapolate stability trends using linear regression.
- **Shelf Life Prediction**: Predict the shelf life using quadratic regression analysis based on user-defined thresholds.
- **PDF Report Generation**: Generate and download comprehensive PDF reports with data tables and plots.
- **Interactive Visualizations**: View original and extrapolated data plots within the app.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/abhipawar2003/Shelf-life-Prediction.git
   cd Shelf-life-Prediction
   ```

2. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application Locally

1. **Ensure MongoDB is connected**:
   Configure your `MONGO_URI` in the `database.py` to point to your MongoDB cluster.
   
   ```python
   MONGO_URI = "mongodb+srv://<username>:<password>@<cluster-url>/Shelf_life_users?retryWrites=true&w=majority"
   ```

2. **Run the Streamlit app**:
   ```bash
   streamlit run app.py
   ```

## Deployment on Streamlit Cloud

1. **Push the code to a GitHub repository**.
2. **Sign in to Streamlit Cloud** and connect the GitHub repo.
3. **Set environment variables** in Streamlit Cloud:
   - Add `MONGO_URI` to the secrets section for secure access.

## Usage

1. **Register/Login**: Create a user account or log in to access the features.
2. **Upload Data**: Upload a CSV file containing columns like `time_months`, `dissolution_%`, and `study_type`.
3. **Extrapolate Data**:
   - Choose the study type (e.g., Accelerated, Real Time).
   - View extrapolated data and download a detailed report.
4. **Predict Shelf Life**:
   - Enter a threshold value (e.g., 75%).
   - View the predicted shelf life and download the report.

## PDF Report Features
- Comprehensive summary of the study.
- Data tables for original and extrapolated data.
- Visual plots of stability profiles.

## Troubleshooting
- Ensure that your browser allows embedded content if the PDF preview is not displayed.
- Verify MongoDB credentials if connection errors occur.

## Technologies Used
- **Python**: Core programming language.
- **Streamlit**: Web application framework.
- **Pandas**: Data manipulation and analysis.
- **Scikit-learn**: Machine learning library for regression models.
- **FPDF**: Library for PDF generation.
- **MongoDB**: Database for storing user and study data.
- **Matplotlib**: Data visualization library.

## Future Enhancements
- Add support for additional machine learning models.
- Integrate data validation and preprocessing features.
- Expand report customization options.

## License
This project is licensed under the MIT License. See `LICENSE` for more details.
