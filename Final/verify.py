import streamlit as st

st.title("Email Verification")

if "email" in st.experimental_get_query_params():
    st.success("Email verified successfully!")
    st.write("Transaction marked as successful.")
    # You can redirect to the main app or process further if needed
else:
    st.error("Invalid or expired verification link.")
