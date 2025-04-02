import streamlit as st

# Must be the first Streamlit command
st.set_page_config(layout="wide")

import urllib.parse
from firebase_auth import init_firebase, verify_user
from date_sum_calculator import date_sum_calculator
from stock_price_calculators import stock_price_at_degree, degrees_from_stock_price
from events_workshops import events_workshops
from blog import blog
from planetary_ingress_date_generator import planetary_ingress_date_generator
from combined_page import combined_numerology_and_dob_analyzer
from orbital_and_gravitational_plotter import orbital_and_gravitational_plotter
from past_predictions import past_predictions
from moon_phase_calculator import moon_phase_calculator
from swing_cycle_projections import run_swing_cycle_projections

def main():
    init_firebase()

    # Read query params but don't print them to the UI
    params = st.query_params
    param_value = params.get("token", [])
    if isinstance(param_value, str):
        param_value = [param_value]

    if not param_value:
        st.warning("Authentication required. Please log in.")
        st.stop()

    raw_token = param_value[-1]

    # URL-decode in case it's encoded
    decoded_token = urllib.parse.unquote(raw_token)

    # Strip out b' prefix if present
    if decoded_token.startswith("b'"):
        decoded_token = decoded_token[2:-1]

    user = verify_user(decoded_token)
    if not user:
        st.warning("Authentication required. Please log in.")
        st.stop()

    # If we reach here, the user is verified
    global_css()
    original_app()

def global_css():
    st.markdown(
        """
        <style>
            .title {
                text-align: center;
                font-size: 3em;
                margin-bottom: 0.1em;
                padding-bottom: 0.5em;
            }
            .bio {
                text-align: center;
                margin-top: 0.1em;
                margin-bottom: 0.1em;
            }
            .bio-details {
                font-size: 1em;
                margin-bottom: 0.1em;
            }
            .bio-details a {
                font-size: 1em;
            }
            .sidebar-content {
                font-size: 1.2em !important;
            }
            .twitter-container {
                display: flex;
                justify-content: center;
                margin-top: 20px;
                width: 100%;
                max-width: 600px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

def original_app():
    st.sidebar.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    app_selection = st.sidebar.radio(
        "Navigation",
        [
            "Home",
            "Numerology & DOB Analyzer",
            "Moon Phase Calculator",
            "Planetary Ingress Dates",
            "Orbital & Gravitational Plotter",
            "Swing & Cycle Projections",
            "Sum of Date Calculator",
            "Stock Price by Degree",
            "Degrees from Stock Price",
            "Events & Workshops",
            "Resource Blog",
            "Past Predictions"
        ],
        index=0,
        key="app_selection"
    )
    st.sidebar.markdown('</div>', unsafe_allow_html=True)

    if app_selection == "Home":
        st.markdown('<div class="title">YASH NENI</div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="bio">
            Time Student, Trader, Astrology and Numerology Enthusiast. 
            Count your blessings only intend to put my thoughts and analysis, 
            always trade at your own risk.
            <br><br>
            <span class="bio-details">
            Location: USA, NYC | 
            Email: <a href="mailto:yashnam15@gmail.com">yashnam15@gmail.com</a> | 
            <a href="https://x.com/YashNeni" target="_blank">X Profile</a>
            </span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.components.v1.html(
            """
            <div class="twitter-container">
                <!-- Embedded tweets or any Home content here -->
            </div>
            """,
            height=1800,
            scrolling=True,
        )

    elif app_selection == "Numerology & DOB Analyzer":
        combined_numerology_and_dob_analyzer()
    elif app_selection == "Moon Phase Calculator":
        moon_phase_calculator()
    elif app_selection == "Planetary Ingress Dates":
        planetary_ingress_date_generator()
    elif app_selection == "Orbital & Gravitational Plotter":
        orbital_and_gravitational_plotter()
    elif app_selection == "Swing & Cycle Projections":
        run_swing_cycle_projections()
    elif app_selection == "Sum of Date Calculator":
        date_sum_calculator()
    elif app_selection == "Stock Price by Degree":
        stock_price_at_degree()
    elif app_selection == "Degrees from Stock Price":
        degrees_from_stock_price()
    elif app_selection == "Events & Workshops":
        events_workshops()
    elif app_selection == "Resource Blog":
        blog()
    elif app_selection == "Past Predictions":
        past_predictions()

if __name__ == "__main__":
    main()
