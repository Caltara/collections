import streamlit as st
import pandas as pd
from collections import send_sms, send_voice
import datetime

st.title("📞 Caltara Collections Agent")

uploaded_file = st.file_uploader("Upload customer CSV", type=["csv"])
method = st.radio("Send via:", ["SMS", "Voice Call"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write(df)

    if st.button("Start Contacting Customers"):
        logs = []
        for _, row in df.iterrows():
            name, phone, amount, due = row['Name'], row['Phone'], row['AmountDue'], row['DueDate']
            try:
                result = send_sms(phone, name, amount, due) if method == "SMS" else send_voice(phone, name, amount, due)
                logs.append({"Name": name, "Phone": phone, "Status": "Sent", "Method": method, "Time": datetime.datetime.now()})
            except Exception as e:
                logs.append({"Name": name, "Phone": phone, "Status": f"Error: {e}", "Method": method, "Time": datetime.datetime.now()})

        log_df = pd.DataFrame(logs)
        st.write("✅ Contact Log", log_df)
        log_df.to_csv("logs.csv", index=False)
