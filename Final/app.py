# Import necessary libraries
import pandas as pd
import joblib
from sklearn.ensemble import IsolationForest
import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Function to train and save the Isolation Forest model
def train_model(csv_path='transaction_data.csv'):
    df = pd.read_csv(csv_path)
    
    # Ensure the 'amount' column exists
    if 'amount' not in df.columns:
        raise ValueError("CSV file must contain an 'amount' column.")
    
    amounts = df['amount'].values.reshape(-1, 1)

    # Initialize the Isolation Forest model with a contamination setting
    model = IsolationForest(contamination=0.01, random_state=42)
    model.fit(amounts)

    # Save the trained model
    joblib.dump(model, 'fraud_detection_model.joblib')
train_model()

#train_model()
# Function to determine if transaction is abnormal using model and threshold
def is_transaction_abnormal(amount, model, threshold=100000):
    if amount > threshold:
        return True  # Automatically flag as abnormal if amount exceeds threshold
    prediction = model.predict([[amount]])
    return prediction[0] == -1

# Function to send verification email
def send_verification_email(user_email):
    sender_email = "thanushreedevi2003@gmail.com"  # Replace with your email
    password = "hbgq tmcl qviw qkom"  # Replace with your app-specific password or Gmail password
    receiver_email = user_email
    
    # Generate a unique verification link for each user
    verification_link = f"http://localhost:8501/verify?email={user_email}"

    message = MIMEMultipart("alternative")
    message["Subject"] = "Transaction Verification"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Email content
    text = "A large transaction was detected. Please verify if it was you by clicking the link below."
    html = f"""
    <html>
      <body>
        <p>A large transaction was detected. Please verify if it was you by clicking the link below:</p>
        <a href="{verification_link}">Verify Transaction</a>
      </body>
    </html>
    """

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)

    # Send email
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        return "Verification email sent successfully."
    except Exception as e:
        return f"Error sending email: {e}"


# Train the model (Run this only once, then comment it out)
train_model()

# Load the trained model
model = joblib.load('fraud_detection_model.joblib')

# Streamlit UI Code
st.title("Wallet Transaction")

# Input field for transaction amount
amount = st.number_input("Enter the transaction amount:", min_value=0)
#user_email = st.text_input("Enter your email for verification (only if flagged):")
user_email = "thanushreedevi2003@gmail.com"

if st.button("Submit Transaction"):
    # Check if transaction is abnormal
    if is_transaction_abnormal(amount, model, threshold=100000):
        st.error("Abnormal Transaction Flagged! Verification required.")
        
        # Send verification email
        email_status = send_verification_email(user_email)
        st.write(email_status)
        #"""if user_email:
         #   email_status = send_verification_email(user_email)
          #  st.write(email_status)
        #else:
         #   st.warning("Please enter your email to receive verification.")"""
    else:
        st.success("Transaction Successful")

# Placeholder for verify page
if "verify" in st.experimental_get_query_params():
    st.write("Thank you for verifying! Transaction confirmed as successful.")
