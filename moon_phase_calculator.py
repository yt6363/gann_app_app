import streamlit as st
import datetime
import swisseph as swe

def calculate_moon_phase(jd):
    # Calculate the moon phase
    moon_lon = swe.calc_ut(jd, swe.MOON, swe.FLG_SWIEPH)[0][0]
    sun_lon = swe.calc_ut(jd, swe.SUN, swe.FLG_SWIEPH)[0][0]
    moon_phase = (moon_lon - sun_lon) % 360
    
    return moon_phase, moon_lon

def zodiac_sign(degree):
    signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
             "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    sign_index = int(degree // 30)
    return signs[sign_index]

def moon_phase_for_ayanamsa(year, month, ayanamsa_mode):
    swe.set_sid_mode(ayanamsa_mode)
    start_date = datetime.date(year, month, 1)
    end_date = (start_date + datetime.timedelta(days=32)).replace(day=1)
    current_date = start_date

    moon_phases = []

    while current_date < end_date:
        jd = swe.julday(current_date.year, current_date.month, current_date.day)
        moon_phase, moon_lon = calculate_moon_phase(jd)
        
        # Use a smaller tolerance to accurately capture New Moon and Full Moon
        if abs(moon_phase) < 1 or abs(moon_phase - 360) < 1:
            phase_name = "New Moon"
        elif abs(moon_phase - 180) < 1:
            phase_name = "Full Moon"
        else:
            current_date += datetime.timedelta(days=1)
            continue
        
        moon_sign = zodiac_sign(moon_lon)
        moon_phases.append((current_date, phase_name, moon_sign))
        current_date += datetime.timedelta(days=1)

    return moon_phases

def moon_phase_calculator():
    st.title("Moon Phase Calculator")
    
    year = st.number_input("Enter the year (e.g., 2024):", min_value=1900, max_value=2100, value=2024)
    month = st.number_input("Enter the month (1-12):", min_value=1, max_value=12, value=7)
    
    ayanamsa_option = st.selectbox("Select the Ayanamsa mode:", ["Sidereal", "Krishnamurthy"])
    
    if ayanamsa_option == "Sidereal":
        ayanamsa_mode = swe.SIDM_LAHIRI
    else:
        ayanamsa_mode = swe.SIDM_KRISHNAMURTI

    if st.button("Calculate Moon Phases"):
        moon_phases = moon_phase_for_ayanamsa(year, month, ayanamsa_mode)
        st.subheader(f"Full Moon and New Moon Phases for {year}-{month} using {ayanamsa_option} Ayanamsa:")
        for date, phase_name, moon_sign in moon_phases:
            st.write(f"{date}: {phase_name} in {moon_sign}")

if __name__ == "__main__":
    moon_phase_calculator()
