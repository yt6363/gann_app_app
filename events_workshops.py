import streamlit as st

def events_workshops():
    st.header("Events and Workshops")
    st.write("Upcoming events and workshops related to astrology, numerology, and trading.")
    
    events = [
        {"name": "Astrology Workshop", "date": "2024-08-01", "location": "New York", "details": "Learn about astrology and how it can help you understand yourself better."},
        {"name": "Numerology Seminar", "date": "2024-09-15", "location": "Los Angeles", "details": "Deep dive into numerology and its applications."},
        {"name": "Trading Strategies with Astrology", "date": "2024-10-05", "location": "Chicago", "details": "Combine trading strategies with astrological insights for better results."}
    ]
    
    for event in events:
        st.subheader(event["name"])
        st.write(f"**Date:** {event['date']}")
        st.write(f"**Location:** {event['location']}")
        st.write(f"**Details:** {event['details']}")
        st.markdown("---")
