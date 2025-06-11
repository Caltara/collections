import streamlit as st
import pandas as pd
from openai import OpenAI
from twilio.rest import Client
import time

# Set up secrets
openai_api_key = st.secrets["OPENAI_API_KEY"]
twilio_sid = st.secrets["TWILIO_ACCOUNT_SID"]
twilio_token = st.secrets["TWILIO_AUTH_TOKEN"]
twilio_phone = st.secrets["TWILIO_PHONE_NUMBER"]

# Initialize clients
openai = OpenAI(api_key=openai_api_key)
twilio_client = Client(twilio_sid, twilio_token)

st.title("📞 AI Collections Agent")

uploaded_file = st.file_uploader("Upload CSV with customer info", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df)

    if st.button("Start Calling Customers"):
        logs = []
        for index, row in df.iterrows():
            name = row['name']
            phone = row['phone']
            amount = row['amount_due']
            due = row['due_date']

            prompt = (
                f"You are a polite but firm collections agent. Call a customer named {name} "
                f"to remind them of a past due payment of ${amount}, due on {due}. "
                f"Keep the message under 45 seconds, and offer for them to call back or pay online."
            )

            try:
                response = openai.chat.completions.create(
                    model="gpt-4o-mini",  # change to "gpt-4" if you have access
                    messages=[{"role": "user", "content": prompt}]
                )
                script = response.choices[0].message.content
                st.write(f"📜 Message for {name}: {script}")

                call = twilio_client.calls.create(
                    twiml=f'<Response><Say voice="alice">{script}</Say></Response>',
                    to=phone,
                    from_=twilio_phone
                )

                logs.append({"name": name, "phone": phone, "status": "Call placed", "sid": call.sid})
                time.sleep(1)

            except Exception as e:
                logs.append({"name": name, "phone": phone, "status": f"Failed: {e}", "sid": None})
                st.error(f"Error with {name}: {e}")

        st.success("✅ All calls attempted.")
        log_df = pd.DataFrame(logs)
        st.dataframe(log_df)

        csv = log_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Call Log", data=csv, file_name="call_log.csv", mime="text/csv")
