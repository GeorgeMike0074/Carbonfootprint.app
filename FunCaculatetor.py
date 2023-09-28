import streamlit as st
import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Declaring global variables
total = None
total1 = None
total_diet = None
total_carbon_footprint = None

# Create a new SQLite database connection and cursor for each thread
def create_db_connection():
    conn = sqlite3.connect('carbon_footprint.db')
    cursor = conn.cursor()

    # Create the 'carbon_footprint' table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS carbon_footprint (
            id INTEGER PRIMARY KEY,
            Electricity_and_Energy_Consumption REAL,
            Transportation_and_Commuting REAL,
            Diet_and_Food_Choices REAL,
            Waste_Management REAL,
            Estimated_Carbon_Footprint REAL
        )
    ''')
    conn.commit()
    return conn, cursor
# Close the SQLite connection
def close_db_connection(conn):
    conn.close()

def household(conn, cursor):
    global total
    noofmembers = st.number_input("Enter Number of Members in your Household", min_value=1)
    electricity = st.number_input("Enter the kWh of Electricity Used")
    naturalgas = st.number_input("Enter kWh of Natural Gas Used ")
    heatingoil = st.number_input("Enter Litres of Heating Oil Used")
    coal = st.number_input("Enter Metric Tons of Coal Used")
    lpg = st.number_input("Enter Litres of LPG Used")
    propane = st.number_input("Enter Litres of Propane Used")
    woodenpellets = st.number_input("Enter Metric Tons of Wooden Pellets Used")
    f_electicity = ((electricity / 1000) * 0.7080)
    f_naturalgas = ((naturalgas / 100) * 0.02)
    f_heatingoil = ((heatingoil / 100) * 0.27)
    f_coal = (coal * 2.88)
    f_lpg = ((lpg / 100) * 0.17)
    f_propane = ((propane / 100) * 0.16)
    f_woodenpellets = (woodenpellets * 0.07)
    total = (f_electicity + f_coal + f_heatingoil + f_lpg + f_naturalgas + f_propane + f_woodenpellets) / noofmembers
    cursor.execute('INSERT INTO carbon_footprint (Electricity_and_Energy_Consumption) VALUES (?)', (total,))
    conn.commit()
    st.title('Your Carbon Footprint is' + " " + str(total) + " " + "Metric Tonnes")


def publictransport(conn, cursor):
    global total1
    bus = ((st.number_input("Enter the Distance Travelled in Bus") / 1000) * 0.10)
    coach = ((st.number_input("Enter the Distance Travelled in Coach") / 1000) * 0.03)
    localtrain = ((st.number_input("Enter the Distance Travelled in Local") / 1000) * 0.04)
    longdistancetrain = ((st.number_input("Enter the Distance Travelled in Long Distance Train") / 10000) * 0.05)
    tram = ((st.number_input("Enter the Distance Travelled in train") / 1000) * 0.03)
    subway = ((st.number_input("Enter the Distance Travelled in subway") / 1000) * 0.03)
    taxi = ((st.number_input("Enter the Distance Travelled in taxi") / 50) * 0.01)
    total1 = (bus + coach + localtrain + longdistancetrain + tram + subway + taxi)
    cursor.execute('INSERT INTO carbon_footprint (Transportation_and_Commuting) VALUES (?)', (total,))
    conn.commit()
    st.title('Your Carbon Footprint is' + " " + str(total1) + " " + "Metric Tonnes")


def carbonfootprint(conn, cursor):
    car_size_options = {
        'Sports car or large SUV (35 mpg)': 35,
        'Small or medium SUV, or MPV (46 mpg)': 46,
        'City, small, medium, large or estate car (52 mpg)': 52
    }
    mileage_options = {
        'Choose an Option': 0,
        'Low (6,000 miles)': 6000,
        'Average (9,000 miles)': 9000,
        'High (12,000 miles)': 12000
    }

    carsize = st.selectbox('Select Car Size', list(car_size_options.keys()))
    carmileage = st.selectbox('Select 12-month car mileage', list(mileage_options.keys()))

    size = car_size_options.get(carsize, 0)
    mileage = mileage_options.get(carmileage, 0)

    carfootprint123 = (((((mileage / size) * 14.3) / 1000) * 0.907185) / 1)
    st.title('Your Carbon Footprint is' + " " + str(carfootprint123) + " " + "Metric Tonnes")


def food(conn, cursor):
    global total_diet
    food_options = {
        'Organic_None': 0.7, 'Organic_Some': 0.5, 'Organic_Most': 0.2,
        'Organic_All': 0, 'Meat_Above-average': 0.6, 'Meat_Average': 0.4,
        'Meat_Below-average': 0.25, 'Lacto-vegetarian': 0.1, 'Vegan': 0,
        'Local_Very little': 0.5, 'Local_Average': 0.3, 'Local_Above average': 0.2,
        'Local_Almost all': 0.1, 'Packaging_Above average': 0.6, 'Packaging_Average': 0.4,
        'Packaging_Below average': 0.2, 'Packaging_Very little': 0.05,
        'Composting_None': 0.2, 'Composting_Some': 0.1, 'Composting_All': 0
    }

    food1 = st.selectbox('How much of the food that you eat is organic?', list(food_options.keys())[0:4])
    food2 = st.selectbox('How much meat/dairy do you eat personally?', list(food_options.keys())[4:9])
    food3 = st.selectbox('How much of your food is produced locally?', list(food_options.keys())[9:13])
    food4 = st.selectbox('How much of your food is packaged or processed?', list(food_options.keys())[13:17])
    food5 = st.selectbox('How much do you compost potato peelings, leftover and unused food etc?', list(food_options.keys())[17:])

    organic = food_options.get(food1, 0)
    meat = food_options.get(food2, 0)
    foodmiles = food_options.get(food3, 0)
    package = food_options.get(food4, 0)
    composting = food_options.get(food5, 0)

    total_diet = (organic + meat + foodmiles + package + composting)
    cursor.execute('INSERT INTO carbon_footprint (Diet_and_Food_Choices) VALUES (?)', (total_diet,))
    conn.commit()
    st.title('Your Carbon Footprint is' + " " + str(total_diet) + " " + "Tonnes")


def estimate_carbon_footprint_from_waste(conn, cursor):
    global total_carbon_footprint
    st.title("Estimate Your Carbon Footprint from Waste")

    # Questions about waste disposal
    st.subheader("Waste Disposal Habits")
    plastic_waste = st.number_input("How many kilograms of plastic waste do you dispose of per week?")
    paper_waste = st.number_input("How many kilograms of paper waste do you dispose of per week?")
    glass_waste = st.number_input("How many kilograms of glass waste do you dispose of per week?")
    metal_waste = st.number_input("How many kilograms of metal waste do you dispose of per week?")
    organic_waste = st.number_input(
        "How many kilograms of organic waste (e.g., food scraps) do you dispose of per week?")

    # Carbon conversion equivalents (sample values in kgCO2/kg of waste)
    carbon_equivalents = {
        "Plastic": 6.0,
        "Paper": 1.0,
        "Glass": 0.6,
        "Metal": 2.5,
        "Organic": 0.2,
    }

    # Calculate carbon footprint based on waste disposal
    total_carbon_footprint = 0
    for waste_type, waste_amount in zip(carbon_equivalents.keys(),
                                        [plastic_waste, paper_waste, glass_waste, metal_waste, organic_waste]):
        if waste_amount > 0:
            carbon_equivalent = carbon_equivalents.get(waste_type, 0)
            carbon_footprint = waste_amount * carbon_equivalent
            total_carbon_footprint += carbon_footprint
        cursor.execute('INSERT INTO carbon_footprint (Waste_Management) VALUES (?)', (total_carbon_footprint,))
        conn.commit()

        # Display the estimated carbon footprint
    st.subheader("Estimated Carbon Footprint from Waste")
    st.write(
        f"Your estimated carbon footprint from waste disposal is approximately {total_carbon_footprint:.2f} kgCO2e "
        f"per year.")


def pico(conn, cursor):
    global total, total1, total_diet, total_carbon_footprint
    st.title("Calculator")
    if st.button("Calculate"):
        # Calculate the total carbon footprint
        total_carbon_footprint = total + total1 + total_diet

        # Insert the total carbon footprint into the database
        cursor.execute('INSERT INTO carbon_footprint (Estimated_Carbon_Footprint) VALUES (?)', (total_carbon_footprint,))
        conn.commit()
        st.success("Data has been recorded!")

        # Display the doughnut chart for the most recent carbon footprint values
        cursor.execute('SELECT * FROM carbon_footprint ORDER BY ID DESC LIMIT 1')  # Select the most recent row
        data = cursor.fetchall()
        if data:
            df = pd.DataFrame(data, columns=['ID', 'Electricity_and_Energy_Consumption', 'Transportation_and_Commuting',
                                             'Diet_and_Food_Choices', 'Waste_Management', 'Estimated_Carbon_Footprint'])
            st.title("Carbon Footprint Breakdown for the Most Recent Entry")

            # Exclude the 'ID' column
            df = df.drop(columns=['ID'])

            # Get the carbon footprint values for the selected variables
            selected_variables = ['Electricity_and_Energy_Consumption', 'Transportation_and_Commuting',
                                  'Diet_and_Food_Choices', 'Waste_Management']
            total_footprint = df.loc[0, selected_variables]

            # Plot a doughnut chart for the carbon footprint breakdown
            plt.figure(figsize=(6, 6))
            plt.title("Carbon Footprint Breakdown")
            plt.pie(total_footprint.values, labels=total_footprint.index, autopct='%1.1f%%', startangle=140,
                    colors=sns.color_palette("Set3"))
            # Draw a circle at the center to make it a doughnut chart
            centre_circle = plt.Circle((0, 0), 0.70, fc='white')
            fig = plt.gcf()
            fig.gca().add_artist(centre_circle)
            plt.axis('equal')
            st.pyplot(plt)
        else:
            st.warning("No data available to plot the doughnut chart.")
    close_db_connection(conn)
