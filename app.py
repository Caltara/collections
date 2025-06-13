import streamlit as st
import pandas as pd
from caltara_agent import send_sms, send_voice
import datetime

st.title("📞 Caltara Collections Agent")

uploaded_file = st.file_uploader("Upload customer CSV", type=["csv"])
method = st.radio("Send via:", ["SMS", "Voice Call"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("📋 Customer Preview", df)

    required_columns = {"Name", "Phone", "AmountDue", "DueDate"}
    if not required_columns.issubset(df.columns):
        st.error(f"❌ CSV must include these columns: {required_columns}")
        st.stop()

    if st.button("Start Contacting Customers"):
        logs = []
        with st.spinner("📡 Contacting customers..."):
            for _, row in df.iterrows():
                name = row['Name']
                phone = str(row['Phone'])
                amount = row['AmountDue']
                due = pd.to_datetime(row['DueDate']).strftime("%B %d, %Y")

                try:
                    result = send_sms(phone, name, amount, due) if method == "SMS" else send_voice(phone, name, amount, due)
                    status = "Sent"
                except Exception as e:
                    status = f"Error: {e}"

                logs.append({
                    "Name": name,
                    "Phone": phone,
                    "Status": status,
                    "Method": method,
                    "Time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })

        log_df = pd.DataFrame(logs)
        st.success("✅ All messages processed.")
        st.write("📊 Contact Log", log_df)
        log_df.to_csv("logs.csv", index=False)
