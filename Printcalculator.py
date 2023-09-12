import sys
import streamlit as st
import sqlite3
import base64
import FuncCaculatetor
from FuncCaculatetor import *

# Create a SQLite database
conn = sqlite3.connect('carbon_footprint.db')
cursor = conn.cursor()

# Create the 'carbon_footprint' table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS carbon_footprint (
        id INTEGER PRIMARY KEY,
        Electricity_and_Energy_Consumption REAL,
        Transportation_and_Commuting REAL,
        Diet_and_Food_Choices REAL,
        Waste_Management REAL
    )
''')
conn.commit()

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = f"""
        <style>
            .stApp {{
                background-image: url("data:image/png;base64,{bin_str}");
                background-size: cover;
            }}
        </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

def main():
    set_background('background.png')

    st.title("Carbon Footprint Calculator")
    options = st.selectbox(
        'Choose Which type of Carbon Footprint do you wanna calculate',
        ('Choose an Option', 'Household Carbon Footprint', 'Public Transport Carbon Footprint', 'Car Carbon Footprint', 'Food Carbon Footprint', "Waste" )
    )
    # Create a dictionary mapping options to corresponding functions
    options_dict = {
        "Household Carbon Footprint": FuncCaculatetor.household,
        "Public Transport Carbon Footprint": FuncCaculatetor.publictransport,
        "Car Carbon Footprint": FuncCaculatetor.carbonfootprint,
        "Food Carbon Footprint": FuncCaculatetor.food,
        "Waste": FuncCaculatetor.estimate_carbon_footprint_from_waste
         }

    # Get the selected option and call the corresponding function using dictionary.get()
    selected_function = options_dict.get(options)
    if selected_function:
        selected_function()
    else:
        print("Invalid option selected.")   
    
if __name__ == '__main__':
    main()
