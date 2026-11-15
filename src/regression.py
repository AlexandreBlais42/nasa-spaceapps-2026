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

    # Use a valid number of cross-validation folds
    cv = min(5, len(X))

    for degree in range(1, max_degree + 1):

        model = make_pipeline(PolynomialFeatures(degree=degree), LinearRegression())

        scores = cross_val_score(model, X, y, cv=cv, scoring="r2")

        results[degree] = scores.mean()

    # Select the best degree
    best_degree = max(results, key=results.get)

    # Train the final model
    model = make_pipeline(PolynomialFeatures(degree=best_degree), LinearRegression())

    model.fit(X, y)

    # Generate predictions
    X_plot = np.linspace(X.min(), X.max(), 300).reshape(-1, 1)
    y_pred = model.predict(X_plot)

    # Create figure
    fig, ax = plt.subplots(figsize=(7, 4))

    ax.scatter(X, y, label="Data")
    ax.plot(X_plot, y_pred, color="red", label="Polynomial regression")

    ax.set_title(f"Polynomial Regression (Degree {best_degree})")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.legend()
    ax.grid()

    return fig, model, best_degree, results
