import streamlit as st
import datetime  # Importing the datetime module
import swisseph as swe

def find_ingress_dates(year, month, latitude, longitude):
    start_date = datetime.date(year, month, 1)
    end_date = (start_date + datetime.timedelta(days=32)).replace(day=1)
    current_date = start_date

    ingress_dates = {planet: [] for planet in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]}
    planet_codes = [swe.SUN, swe.MOON, swe.MARS, swe.MERCURY, swe.JUPITER, swe.VENUS, swe.SATURN]

    swe.set_sid_mode(swe.SIDM_KRISHNAMURTI)

    while current_date < end_date:
        jd = swe.julday(current_date.year, current_date.month, current_date.day)
        for planet, code in zip(ingress_dates.keys(), planet_codes):
            lon = swe.calc_ut(jd, code, swe.FLG_SIDEREAL)[0][0]
            next_day = current_date + datetime.timedelta(days=1)
            jd_next = swe.julday(next_day.year, next_day.month, next_day.day)
            lon_next = swe.calc_ut(jd_next, code, swe.FLG_SIDEREAL)[0][0]
            if int(lon // 30) != int(lon_next // 30):
                ingress_dates[planet].append((next_day, int(lon_next // 30) + 1))
        current_date += datetime.timedelta(days=1)

    return ingress_dates

def find_all_ingress_dates(year, planet_code, latitude, longitude):
    start_date = datetime.date(year, 1, 1)
    end_date = datetime.date(year + 1, 1, 1)
    current_date = start_date

    ingress_dates = []

    swe.set_sid_mode(swe.SIDM_KRISHNAMURTI)

    while current_date < end_date:
        jd = swe.julday(current_date.year, current_date.month, current_date.day)
        lon = swe.calc_ut(jd, planet_code, swe.FLG_SIDEREAL)[0][0]
        next_day = current_date + datetime.timedelta(days=1)
        jd_next = swe.julday(next_day.year, next_day.month, next_day.day)
        lon_next = swe.calc_ut(jd_next, planet_code, swe.FLG_SIDEREAL)[0][0]
        if int(lon // 30) != int(lon_next // 30):
            ingress_dates.append((next_day, int(lon_next // 30) + 1))
        current_date += datetime.timedelta(days=1)

    return ingress_dates

def get_lat_long(country):
    coordinates = {
        'USA': {
            'New York': (40.7128, -74.0060),
            'Los Angeles': (34.0522, -118.2437),
            'Chicago': (41.8781, -87.6298),
            'Houston': (29.7604, -95.3698)
        },
        'India': {
            'Delhi': (28.7041, 77.1025),
            'Mumbai': (19.0760, 72.8777),
            'Bangalore': (12.9716, 77.5946),
            'Chennai': (13.0827, 80.2707)
        }
    }
    return coordinates[country]

def planetary_ingress_date_generator():
    st.title("Planetary Ingress date calculator")
    
    year = st.number_input("Enter the year (e.g., 2024):", min_value=2000, max_value=2100, value=2024)
    month = st.number_input("Enter the month (1-12):", min_value=1, max_value=12, value=7)
    
    country = st.selectbox("Select the country:", ['USA', 'India'])
    
    cities_dict = get_lat_long(country)
    city = st.selectbox("Select the city:", list(cities_dict.keys()))
    latitude, longitude = cities_dict[city]

    choice = st.radio("Select the option:", 
                      ["Ingress dates for all planets in the specified month", 
                       "Ingress dates for a specific planet for the entire year"])
    
    if choice == "Ingress dates for all planets in the specified month":
        ingress_dates = find_ingress_dates(year, month, latitude, longitude)
        st.subheader(f"Ingress dates for all planets in {year}-{month}:")
        for planet, dates in ingress_dates.items():
            for date, sign in dates:
                st.write(f"{planet} enters sign {sign} on {date}")
    else:
        planet_name_to_code = {
            "Sun": swe.SUN,
            "Moon": swe.MOON,
            "Mars": swe.MARS,
            "Mercury": swe.MERCURY,
            "Jupiter": swe.JUPITER,
            "Venus": swe.VENUS,
            "Saturn": swe.SATURN
        }

        planet_name = st.selectbox("Select the planet:", list(planet_name_to_code.keys()))
        planet_code = planet_name_to_code[planet_name]

        st.subheader(f"All ingress dates for {planet_name} in {year}:")
        all_ingress_dates = find_all_ingress_dates(year, planet_code, latitude, longitude)
        for date, sign in all_ingress_dates:
            st.write(f"{planet_name} enters sign {sign} on {date}")
