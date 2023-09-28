import streamlit as st
import base64
import FunCaculatetor
from FunCaculatetor import *


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

    # Create a database connection and cursor
    conn, cursor = create_db_connection()

    set_background('background - Edited.png')

    st.title("Carbon Footprint Calculator")
    options = st.selectbox(
        'Choose Which type of Carbon Footprint do you wanna calculate',
        ('Choose an Option', 'Household Carbon Footprint', 'Public Transport Carbon Footprint', 'Car Carbon Footprint',
         'Food Carbon Footprint', "Waste")
    )
    # Create a dictionary mapping options to corresponding functions
    options_dict = {
        "Household Carbon Footprint": FunCaculatetor.household,
        "Public Transport Carbon Footprint": FunCaculatetor.publictransport,
        "Car Carbon Footprint": FunCaculatetor.carbonfootprint,
        "Food Carbon Footprint": FunCaculatetor.food,
        "Waste": FunCaculatetor.estimate_carbon_footprint_from_waste
    }
    # Get the selected option and call the corresponding function using dictionary.get()
    selected_function = options_dict.get(options)
    if selected_function:
        selected_function(conn, cursor)
    else:
         print("Invalid option selected.")
         
         
    pico(conn, cursor)


if __name__ == '__main__':
    main()
