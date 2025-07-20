import streamlit as st
import speech_recognition as sr
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import pandas as pd
import os

# Load CSS
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("style.css")

# Google Sheets setup
def connect_gsheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("Expense Tracker").sheet1
    return sheet

# Voice recognition
def get_voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎙️ Listening... Speak your expense (e.g., 'Add 300 for groceries')")
        audio = recognizer.listen(source, timeout=5)

    try:
        st.success("🔊 Recognizing...")
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        st.error("❌ Could not understand audio.")
    except sr.RequestError:
        st.error("⚠️ API request error.")
    return ""

# Parse voice command
def parse_expense(command):
    words = command.lower().split()
    amount = None
    category = None

    for word in words:
        if word.isdigit():
            amount = int(word)
            break

    if "for" in words:
        idx = words.index("for")
        category = " ".join(words[idx+1:])

    return amount, category

# Add to Google Sheet
def add_expense(amount, category, description):
    sheet = connect_gsheet()
    sheet.append_row([str(datetime.now()), category, amount, description])
    st.success(f"✅ Added: ₹{amount} for {category}")

# Show history
def show_history():
    sheet = connect_gsheet()
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    if not df.empty:
        st.subheader("📊 Expense History")
        st.dataframe(df)

        chart = df.groupby("Category")["Amount"].sum().plot(kind="barh", title="Expenses by Category")
        st.pyplot(chart.figure)
    else:
        st.warning("No expenses recorded yet.")

# Streamlit UI
st.title("💸 Voice-Controlled Expense Tracker")

if st.button("🎤 Record Expense"):
    voice_text = get_voice_input()
    if voice_text:
        amount, category = parse_expense(voice_text)
        if amount and category:
            add_expense(amount, category, voice_text)
        else:
            st.warning("⚠️ Couldn't parse amount or category from your voice.")

st.markdown("---")
show_history()
