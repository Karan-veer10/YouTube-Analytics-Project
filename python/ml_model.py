import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import os

# ✅ Load dataset
file_path = os.path.join("..", "data", "processed", "YouTubeData_Cleaned.csv")

if not os.path.exists(file_path):
    raise FileNotFoundError(f"CSV file not found at {file_path}")

df = pd.read_csv(file_path)
print("✅ Dataset loaded successfully!")
print(df.head())

# ✅ Convert UploadDate to datetime
df["UploadDate"] = pd.to_datetime(df["UploadDate"], errors="coerce")

# ✅ Feature engineering: extract time features
df["UploadDay"] = df["UploadDate"].dt.day
df["UploadMonth"] = df["UploadDate"].dt.month
df["UploadHour"] = df["UploadDate"].dt.hour
df["UploadDayOfWeek"] = df["UploadDate"].dt.dayofweek

# ✅ Handle missing values (if any)
df = df.dropna(subset=["Views", "Likes", "Comments"])

# ✅ Log-transform Views (target variable)
df["LogViews"] = np.log1p(df["Views"])  # log(views + 1)

# ✅ Features and target
X = df[["Likes", "Comments", "UploadDay", "UploadMonth", "UploadHour", "UploadDayOfWeek"]]
y = df["LogViews"]

# ✅ Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ✅ Train RandomForest model
model = RandomForestRegressor(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# ✅ Predictions
y_pred = model.predict(X_test)

# ✅ Evaluate performance (convert back from log scale)
mse = mean_squared_error(np.expm1(y_test), np.expm1(y_pred))
r2 = r2_score(np.expm1(y_test), np.expm1(y_pred))

print("\n📊 Model Evaluation with RandomForest:")
print(f"Mean Squared Error: {mse}")
print(f"R² Score: {r2}")

# ✅ Example prediction
sample_input = pd.DataFrame({
    "Likes": [200],
    "Comments": [10],
    "UploadDay": [15],
    "UploadMonth": [8],
    "UploadHour": [16],
    "UploadDayOfWeek": [4]  # Friday
})
predicted_views = np.expm1(model.predict(sample_input))[0]

print(f"\n🔮 Predicted Views for sample input: {int(predicted_views)}")
