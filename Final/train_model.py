import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib

# Function to train the Isolation Forest model and save it
def train_model(csv_path):
    df = pd.read_csv(csv_path)
    
    # Ensure the 'amount' column exists
    if 'amount' not in df.columns:
        raise ValueError("CSV file must contain an 'amount' column.")
    
    amounts = df['amount'].values.reshape(-1, 1)

    # Initialize the Isolation Forest model with adjusted contamination
    model = IsolationForest(contamination=0.05, random_state=42)
    model.fit(amounts)

    # Save the model for use in the Streamlit app
    joblib.dump(model, 'fraud_detection_model.joblib')

# Function to predict and add a direct threshold check
def is_transaction_abnormal(amount, model, threshold=100000):
    # Check if the transaction amount is above a hard-coded threshold
    if amount > threshold:
        return True  # Automatically flag as abnormal

    # Use the trained model to check for anomalies
    prediction = model.predict([[amount]])
    return prediction[0] == -1

# Load and train the model
csv_path = 'transaction_data.csv'  # Your CSV file path
train_model(csv_path)
print("Model trained and saved.")
