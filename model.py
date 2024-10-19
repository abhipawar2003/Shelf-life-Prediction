import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Extrapolation using Linear Regression
def extrapolate_data(data):
    model = LinearRegression()
    X = data[['time_months']].values
    y = data['dissolution_%'].values
    model.fit(X, y)

    # Extrapolating from 7 to 24 months
    future_months = pd.DataFrame({'time_months': range(7, 25)})
    predicted_dissolution = model.predict(future_months)
    future_months['predicted_dissolution'] = predicted_dissolution

    # Plot the data
    plt.figure(figsize=(10, 6))
    plt.plot(data['time_months'], data['dissolution_%'], 'bo-', label="Original Data")
    plt.plot(future_months['time_months'], future_months['predicted_dissolution'], 'ro--', label="Extrapolated Data")
    plt.xlabel('Time (Months)')
    plt.ylabel('Dissolution (%)')
    plt.title('Dissolution Over Time')
    plt.legend()
    plt.grid(True)

    # Save the plot as an image file
    plot_path = "extrapolated_plot.png"
    plt.savefig(plot_path)
    plt.close()

    return future_months, plot_path

# Predict Shelf Life using Quadratic Regression
def predict_shelf_life(extrapolated_data):
    # Fit a quadratic regression model
    X = extrapolated_data['time_months'].values
    y = extrapolated_data['predicted_dissolution'].values

    # Fit quadratic model using numpy's polyfit for a 2nd degree polynomial (quadratic)
    quadratic_coeffs = np.polyfit(X, y, 2)
    quadratic_model = np.poly1d(quadratic_coeffs)
    
    # Predict dissolution over time using the quadratic model
    future_months = pd.DataFrame({'time_months': range(6, 100)})  # Predicting dissolution for 6 to 100 months
    future_months['predicted_dissolution'] = quadratic_model(future_months['time_months'])

    # Determine when the dissolution drops below 75%
    below_75 = future_months[future_months['predicted_dissolution'] < 75]

    if not below_75.empty:
        return below_75['time_months'].min()  # Return the first month when it drops below 75%
    else:
       return "Shelf life exceeds 100 months"
