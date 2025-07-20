import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import pandas as pd
import json

# Load CSS
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("style.css")

# Connect to Google Sheets using Streamlit secrets
def connect_gsheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_dict = json.loads(st.secrets["GOOGLE_SHEETS_CREDS"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    sheet = client.open("Expense Tracker").sheet1
    return sheet

# Parse simple input like: "Add 200 for food"
def parse_expense(text):
    words = text.lower().split()
    amount = None
    category = None

    for word in words:
        if word.isdigit():
            amount = int(word)
            break

    if "for" in words:
        idx = words.index("for")
        category = " ".join(words[idx + 1:])
    
    return amount, category

# Add expense to Google Sheet
def add_expense(amount, category, description):
    sheet = connect_gsheet()
    sheet.append_row([str(datetime.now()), category, amount, description])
    st.success(f"✅ Added ₹{amount} for {category}")

# Show expense table + chart
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

# UI
st.title("💸 Expense Tracker (Cloud Version)")
st.markdown("Enter your expense below (e.g., `Add 500 for groceries`)")

user_input = st.text_input("📝 Enter Expense")
if st.button("Submit"):
    if user_input:
        amount, category = parse_expense(user_input)
        if amount and category:
            add_expense(amount, category, user_input)
        else:
            st.warning("⚠️ Couldn't extract amount or category from input.")

st.markdown("---")
show_history()
