import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression


def polynomial_regression(x, y, max_degree=9):

    # Convert data to numpy arrays
    X = np.array(x).reshape(-1, 1)
    y = np.array(y)

    # Test different polynomial degrees
    results = {}

    for degree in range(1, max_degree + 1):

        model = make_pipeline(PolynomialFeatures(degree=degree), LinearRegression())

        # Perform cross-validation
        scores = cross_val_score(model, X, y, cv=5, scoring="r2")

        results[degree] = scores.mean()

        print(f"Degree {degree}: R² = {scores.mean():.3f}")

    # Select the best degree
    best_degree = max(results, key=results.get)

    print(f"\nBest degree: {best_degree}")

    # Train the final model
    model = make_pipeline(PolynomialFeatures(degree=best_degree), LinearRegression())

    model.fit(X, y)

    # Generate predictions
    X_plot = np.linspace(X.min(), X.max(), 300).reshape(-1, 1)
    y_pred = model.predict(X_plot)

    # Calculate R²
    r2 = model.score(X, y)

    # Display results
    plt.figure(figsize=(9, 5))
    plt.scatter(X, y, label="Data")
    plt.plot(X_plot, y_pred, color="red", label="Polynomial regression")

    plt.title(f"Polynomial Regression (Degree {best_degree})")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend()
    plt.grid()
    plt.show()

    print(f"R² (training): {r2:.3f}")

    return model, best_degree, results
