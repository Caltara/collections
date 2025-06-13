import streamlit as st
from caltara_agent import send_sms, send_voice
from twilio_server import app as twilio_app
from fastapi import FastAPI
from streamlit.web.server import Server

# Streamlit UI
st.title("📞 Caltara AI Collections Agent")

to = st.text_input("📱 Customer Phone Number", "+1")
name = st.text_input("👤 Customer Name")
amount = st.text_input("💵 Amount Due", "125")
due_date = st.date_input("📅 Due Date")
domain_url = "https://collections-dvpk.onrender.com"

if st.button("Send SMS Reminder"):
    result = send_sms(to, name, amount, due_date)
    st.success(f"✅ SMS sent! SID: {result.sid}")

if st.button("Make Voice Call"):
    if not domain_url:
        st.error("❌ Please enter your public webhook domain URL.")
    else:
        result = send_voice(to, name, amount, due_date, domain_url)
        st.success(f"📞 Voice call started! SID: {result.sid}")

# OPTIONAL: Run FastAPI server if you’re embedding
# (You’ll still need to run the FastAPI server on a public endpoint for Twilio)
