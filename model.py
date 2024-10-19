# import pandas as pd
# from sklearn.linear_model import LinearRegression

# def extrapolate_data(data):
#     model = LinearRegression()
#     X = data[['time_months']].values
#     y = data['dissolution_%'].values
#     model.fit(X, y)

#     future_months = pd.DataFrame({'time_months': range(6, 25)})
#     predicted_dissolution = model.predict(future_months)
#     future_months['predicted_dissolution'] = predicted_dissolution

#     return future_months

# def predict_shelf_life(data):
#     model = LinearRegression()
#     X = data[['time_months']].values
#     y = data['dissolution_%'].values
#     model.fit(X, y)

#     future_months = pd.DataFrame({'time_months': range(6, 61)})
#     predicted_dissolution = model.predict(future_months)

#     below_75 = future_months[predicted_dissolution < 75]
#     if not below_75.empty:
#         return below_75['time_months'].min()
#     else:
#         return "Shelf life exceeds 60 months"

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# Extrapolation using Linear Regression
def extrapolate_data(data):
    model = LinearRegression()
    X = data[['time_months']].values
    y = data['dissolution_%'].values
    model.fit(X, y)

    future_months = pd.DataFrame({'time_months': range(6, 25)})  # Extrapolating from 6 to 24 months
    predicted_dissolution = model.predict(future_months)
    future_months['predicted_dissolution'] = predicted_dissolution

    return future_months

# Predict Shelf Life using Quadratic Regression
def predict_shelf_life(data):
    # Fit a quadratic regression model
    X = data['time_months'].values
    y = data['dissolution_%'].values

    # Fit quadratic model using numpy's polyfit for a 2nd degree polynomial (quadratic)
    quadratic_coeffs = np.polyfit(X, y, 2)
    quadratic_model = np.poly1d(quadratic_coeffs)
    
    # Predict dissolution over time using the quadratic model
    future_months = pd.DataFrame({'time_months': range(6, 100)})  # Predicting dissolution for 6 to 60 months
    future_months['predicted_dissolution'] = quadratic_model(future_months['time_months'])

    # Determine when the dissolution drops below 75%
    below_75 = future_months[future_months['predicted_dissolution'] < 75]

    if not below_75.empty:
        return below_75['time_months'].min()  # Return the first month when it drops below 75%
    else:
        return "Shelf life exceeds 60 months"

# Example usage
if __name__ == "__main__":
    # Sample data for demonstration
    data = {
        'time_months': [0, 1, 2, 3, 6],
        'dissolution_%': [100.81, 99.19, 98.39, 97.75, 96.13]
    }

    df = pd.DataFrame(data)

    # Extrapolate data using Linear Regression
    extrapolated_data = extrapolate_data(df)
    print("Extrapolated Data:\n", extrapolated_data)

    # Predict shelf life using Quadratic Regression
    shelf_life = predict_shelf_life(df)
    print("Predicted Shelf Life:", shelf_life)
