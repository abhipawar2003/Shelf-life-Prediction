from sklearn.metrics import mean_squared_error, accuracy_score

# Data from the provided table
extrapolated_dissolution = [100.428, 98.754, 97.08, 95.406, 93.732]
actual_dissolution = [100.81, 98.73, 98.73, 97.65, 93.33]

# Calculate MSE
mse = mean_squared_error(actual_dissolution, extrapolated_dissolution)
print(f"Mean Squared Error (MSE): {mse}")

# Define a threshold for accuracy (for example, within 0.5 for being considered 'correct')
threshold = 2.221
correct_predictions = [abs(a - e) < threshold for a, e in zip(actual_dissolution, extrapolated_dissolution)]

# Calculate accuracy
accuracy = accuracy_score([True] * len(actual_dissolution), correct_predictions)
print(f"Accuracy: {accuracy * 100:.2f}%")
