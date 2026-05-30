import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
from datetime import datetime


cancellations_df = pd.read_csv(r"C:\Users\Mimansak Nepal\Documents\The Lukla Weather Risk Dashboard\backend\cancellations.csv")
weather_df = pd.read_csv("processed.csv")


df = pd.merge(cancellations_df,weather_df, on = "date")
print(f"Merged Sucessfully!")

df['date'] = pd.to_datetime(df['date'])
df['Month'] = df['date'].dt.month

df['date'] = pd.to_datetime(df['date'])
df['Month'] = df['date'].dt.month

df = df.drop(columns=["date"])

X = df.drop(columns=["Cancelled"])
y = df["Cancelled"]

X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.2,random_state=42)

model = xgb.XGBClassifier(random_state = 42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy*100:.2f}%")

joblib.dump(model, "model.joblib")
print("Saved!")

