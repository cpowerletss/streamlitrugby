import sqlite3
import pandas as pd
import streamlit as st

# Connect to the database file
conn = sqlite3.connect("rugby.db")

st.title("Rugby Players")

# ---------- Part 1: Add a player ----------
st.header("Add a player")

# Get the lists of positions and countries for the drop-down boxes
position_rows = conn.execute("SELECT position_name FROM positions").fetchall()
country_rows = conn.execute("SELECT country_name FROM countries").fetchall()
positions = [row[0] for row in position_rows]
countries = [row[0] for row in country_rows]

# Input boxes
name = st.text_input("Name")
age = st.number_input("Age", min_value=16, max_value=50, value=25)
caps = st.number_input("Caps", min_value=0, value=0)
position = st.selectbox("Position", positions)
country = st.selectbox("Country", countries)

# This code only runs when the button is clicked
if st.button("Add player"):
    if name == "":
        st.error("Please enter a name")
    else:
        # The two (SELECT ...) parts turn the position and country names into ID numbers
        conn.execute(
            """INSERT INTO players (name, age, caps, position_id, country_id)
               VALUES (?, ?, ?,
                       (SELECT position_id FROM positions WHERE position_name = ?),
                       (SELECT country_id FROM countries WHERE country_name = ?))""",
            (name, age, caps, position, country),
        )
        conn.commit()
        st.success("Added " + name)

# ---------- Part 2: Show all players ----------
st.header("All players")

table = pd.read_sql_query(
    "SELECT name, age, caps, position, country FROM player_details ORDER BY name", conn
)
st.dataframe(table, hide_index=True)