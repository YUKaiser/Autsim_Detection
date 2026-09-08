import joblib
import pandas as pd


# Load trained models
child_model = joblib.load("models/child_model.pkl")
adult_model = joblib.load("models/adult_model.pkl")


# The order MUST remain exactly the same
FEATURES = [
    "A1_Score",
    "A2_Score",
    "A3_Score",
    "A4_Score",
    "A5_Score",
    "A6_Score",
    "A7_Score",
    "A8_Score",
    "A9_Score",
    "A10_Score"
]


def predict_behavioral(age, answers):

    # Check that exactly 10 answers are provided
    if len(answers) != 10:
        raise ValueError("Exactly 10 behavioral answers are required.")

    # Check answers are 0 or 1
    if any(answer not in [0, 1] for answer in answers):
        raise ValueError("Each answer must be either 0 or 1.")

    # Select model based on age
    if 4 <= age <= 11:
        model = child_model

    elif age >= 18:
        model = adult_model

    else:
        raise ValueError(
            "This model currently supports ages 4-11 and 18+."
        )

    # Convert answers into model input
    X = pd.DataFrame(
    [answers],
    columns=FEATURES
)

    # Prediction
    prediction = model.predict(X)[0]

    # Probability
    probability = model.predict_proba(X)[0][1]

    # Behavioral score
    score = sum(answers)

    return {
        "score": score,
        "prediction": "YES" if prediction == 1 else "NO",
        "probability": probability
    }

if __name__ == "__main__":

    answers = [
        1, 1, 1, 0, 1,
        1, 0, 1, 0, 1
    ]

    # Test child
    print("\n--- CHILD TEST ---")

    result = predict_behavioral(
        age=8,
        answers=answers
    )

    print(result)


    # Test adult
    print("\n--- ADULT TEST ---")

    result = predict_behavioral(
        age=25,
        answers=answers
    )

    print(result)


    # Test unsupported age
    print("\n--- TEENAGER TEST ---")

    try:
        result = predict_behavioral(
            age=15,
            answers=answers
        )

        print(result)

    except ValueError as e:
        print("Error:", e)