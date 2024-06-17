
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR


# Sample data (replace with your actual calculated and experimental shifts)
calculated_shifts = np.array([4.4985, 4.4105, 4.4782, 8.2011, 4.7663, 3.4197, 3.4236, 4.5794, 3.7526, 3.7502 ])
experimental_shifts = np.array([4.0000, 4.0000, 4.0000, 7.5100, 3.4100, 3.4100, 3.4100, 3.5900, 3.5900, 3.5900])

# Reshape calculated shifts (if needed)
calculated_shifts = calculated_shifts.reshape(-1, 1)


# ... (rest of your code as before)

# Create an SVR model with linear kernel (adjust kernel if needed)
model = SVR(kernel='linear')

# Fit the model on the data
model.fit(calculated_shifts, experimental_shifts)

# Predict scaled values using the fitted model
scaled_calculated_shifts = model.predict(calculated_shifts)

# Print the predicted scaled values
print("Scaled calculated shifts:", scaled_calculated_shifts.flatten())

