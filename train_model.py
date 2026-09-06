import pandas as pd
import joblib
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

# ============================================
# FEATURES
# ============================================

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

def rule_based_prediction(df):

    score = df[FEATURES].sum(axis=1)

    prediction = (score >= 7).astype(int)

    return prediction

# ============================================
# FUNCTION TO TRAIN MODEL
# ============================================

def train_model(df, model_name):

    print("\n================================")
    print(model_name)
    print("================================")

    # ----------------------------------------
    # 1. Remove duplicate rows
    # ----------------------------------------

    df = df.drop_duplicates()

    print("Dataset shape after duplicates removed:")
    print(df.shape)

    # ----------------------------------------
    # 2. Create X
    # ----------------------------------------

    X = df[FEATURES]

    # ----------------------------------------
    # 3. Create y
    # NO  -> 0
    # YES -> 1
    # ----------------------------------------

    y = (df["Class/ASD"] == "YES").astype(int)

    print("\nTarget distribution:")
    print(y.value_counts())

    rule_pred = rule_based_prediction(df)

    rule_accuracy = accuracy_score(y, rule_pred)

    print("\nRule-Based Accuracy:", rule_accuracy)

    # ----------------------------------------
    # 4. Train/Test Split
    # ----------------------------------------

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )

    print("\nTraining samples:", len(X_train))
    print("Testing samples:", len(X_test))

    # ----------------------------------------
    # 5. Create Logistic Regression model
    # ----------------------------------------

    model = LogisticRegression(
        max_iter=1000
    )

    # ----------------------------------------
    # 6. Train
    # ----------------------------------------

    model.fit(X_train, y_train)
    print("\nModel Coefficients:")

    for feature, coefficient in zip(FEATURES, model.coef_[0]):
        print(f"{feature}: {coefficient:.4f}")

    cv_scores = cross_val_score(
    model,
    X,
    y,
    cv=5,
    scoring="accuracy"
)
    print("\n5-Fold Cross Validation:")
    print("Scores:", cv_scores)
    print("Mean:", cv_scores.mean())
    # ----------------------------------------
    # 7. Predict
    # ----------------------------------------

    y_pred = model.predict(X_test)

    # ----------------------------------------
    # 8. Evaluation
    # ----------------------------------------

    print("\n========== MODEL EVALUATION ==========")

    print(
        "Accuracy:",
        accuracy_score(y_test, y_pred)
    )

    print(
        "Precision:",
        precision_score(y_test, y_pred)
    )

    print(
        "Recall:",
        recall_score(y_test, y_pred)
    )

    print(
        "F1 Score:",
        f1_score(y_test, y_pred)
    )

    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    print("\nClassification Report:")
    print(classification_report(
        y_test,
        y_pred,
        target_names=["NO", "YES"]
    ))

    return model


# ============================================
# LOAD DATASETS
# ============================================

child_df = pd.read_excel(
    "data/child_autism_dataset.xlsx"
)

adult_df = pd.read_csv(
    "data/autism_screening.csv"
)


# ============================================
# TRAIN CHILD MODEL
# ============================================

child_model = train_model(
    child_df,
    "CHILD MODEL"
)
joblib.dump(
    child_model,
    "models/child_model.pkl"
)

# ============================================
# TRAIN ADULT MODEL
# ============================================

adult_model = train_model(
    adult_df,
    "ADULT MODEL"
)

joblib.dump(
    adult_model,
    "models/adult_model.pkl"
)