import streamlit as st
import numpy as np
import plotly.graph_objs as go
from astropy.time import Time
from astropy.coordinates import solar_system_ephemeris, get_body, get_sun, SkyCoord, GCRS
from astropy.constants import G, M_sun, M_earth
import certifi
import os
from datetime import datetime, timedelta

# Set SSL_CERT_FILE to use certifi's certificate bundle
os.environ['SSL_CERT_FILE'] = certifi.where()

# Define the path to the local ephemeris file
EPHEMERIS_PATH = os.path.join(os.getcwd(), 'de421.bsp')

# Custom get_moon function
def get_moon(time):
    """
    Replacement for the removed `get_moon` function in Astropy.
    Returns the position of the Moon in GCRS coordinates.
    """
    with solar_system_ephemeris.set("builtin"):
        moon_position = get_body("moon", time)
    return moon_position

def orbital_speed(distance, mu):
    return np.sqrt(mu / distance)

def gravitational_force(mass1, mass2, distance):
    return (G.value * mass1 * mass2) / (distance ** 2)

def get_declination(obj, time):
    if obj == 'sun':
        obj_position = get_sun(time)
    elif obj == 'moon':
        obj_position = get_moon(time)
    else:
        with solar_system_ephemeris.set(EPHEMERIS_PATH):
            obj_position = get_body(obj, time)
    
    sky_coord = SkyCoord(obj_position)
    gcrs_coord = sky_coord.transform_to(GCRS(obstime=time))
    return gcrs_coord.dec.degree

def get_object_position(obj, time):
    if obj == 'sun':
        return get_sun(time)
    elif obj == 'moon':
        return get_moon(time)
    else:
        with solar_system_ephemeris.set(EPHEMERIS_PATH):
            return get_body(obj, time)

def plot_data(objects, duration_unit, duration_value, start_date, plot_speed, plot_grav_force, plot_declination):
    # Convert duration to days
    duration_days = {
        'years': duration_value * 365,
        'months': duration_value * 30,
        'weeks': duration_value * 7,
        'days': duration_value
    }.get(duration_unit, None)
    if duration_days is None:
        raise ValueError("Invalid duration unit. Please enter 'years', 'months', 'weeks', or 'days'.")

    # Convert start_date to the correct format for Time
    observation_start_time = Time(start_date.strftime('%Y-%m-%d'))

    # Create an array of observation times over the specified duration
    observation_times = Time(np.linspace(observation_start_time.jd, observation_start_time.jd + duration_days, duration_days), format='jd')

    # Masses of the planets and Moon (in kg)
    object_masses = {
        'mercury': 3.3011e23,
        'venus': 4.8675e24,
        'earth': 5.97237e24,
        'mars': 6.4171e23,
        'jupiter': 1.8982e27,
        'saturn': 5.6834e26,
        'uranus': 8.6810e25,
        'neptune': 1.02413e26,
        'moon': M_earth.value * 0.0123,  # Approximate mass of the Moon
        'sun': M_sun.value
    }

    mu = G.value * M_sun.value  # Gravitational parameter for the Sun

    # Create Plotly figure
    fig = go.Figure()

    # Plot orbital speed
    if plot_speed:
        for obj in objects:
            if obj not in object_masses:
                st.error(f"Unknown object: {obj}")
                continue

            speeds = []
            for t in observation_times:
                obj_position = get_object_position(obj, t)
                distance = obj_position.distance.to('m').value
                speed = orbital_speed(distance, mu)
                speeds.append(speed)

            speeds = np.array(speeds)
            normalized_speeds = (speeds - np.min(speeds)) / (np.max(speeds) - np.min(speeds))
            fig.add_trace(go.Scatter(x=observation_times.datetime, y=normalized_speeds, mode='lines', name=f'{obj.capitalize()} Orbital Speed'))

    # Plot gravitational force
    if plot_grav_force:
        for obj in objects:
            if obj not in object_masses:
                st.error(f"Unknown object: {obj}")
                continue

            mass = object_masses[obj]
            forces = []
            for t in observation_times:
                obj_position = get_object_position(obj, t)
                distance = obj_position.distance.to('m').value
                force = gravitational_force(mass, M_sun.value, distance)
                forces.append(force)

            forces = np.array(forces)
            normalized_forces = (forces - np.min(forces)) / (np.max(forces) - np.min(forces))
            fig.add_trace(go.Scatter(x=observation_times.datetime, y=normalized_forces, mode='lines', name=f'{obj.capitalize()} Gravitational Force'))

    # Plot declination
    if plot_declination:
        for obj in objects:
            declinations = []
            for t in observation_times:
                dec = get_declination(obj, t)
                declinations.append(dec)

            declinations = np.array(declinations)
            normalized_declinations = (declinations - np.min(declinations)) / (np.max(declinations) - np.min(declinations))
            fig.add_trace(go.Scatter(x=observation_times.datetime, y=normalized_declinations, mode='lines', name=f'{obj.capitalize()} Declination'))

    # Add today's date as a vertical dotted line if within the range
    today = datetime.today()
    if observation_start_time.datetime <= today <= observation_start_time.datetime + timedelta(days=duration_days):
        fig.add_trace(go.Scatter(x=[today, today], y=[0, 1], mode='lines', name="Today", line=dict(dash='dot', color='red')))

    fig.update_layout(title='Orbital and Gravitational Data', xaxis_title='Date', yaxis_title='Normalized Values', hovermode='x unified')
    
    st.plotly_chart(fig)

def orbital_and_gravitational_plotter():
    st.title("Orbital and Gravitational Plotter")

    objects_input = st.text_input("Enter the object names (e.g., 'mars,jupiter,sun,moon')", placeholder="mars, jupiter, sun")
    duration_unit = st.selectbox("Select the duration unit", ["years", "months", "weeks", "days"])
    duration_value = st.number_input("Enter the number of duration units", min_value=1, value=1)
    start_date = st.date_input("Enter the start date")

    plot_speed = st.checkbox("Orbital Speed", value=True)
    plot_grav_force = st.checkbox("Gravitational Force", value=True)
    plot_declination = st.checkbox("Declination", value=True)

    if st.button("Submit"):
        objects = objects_input.strip().lower().split(',')
        plot_data(objects, duration_unit, duration_value, start_date, plot_speed, plot_grav_force, plot_declination)

orbital_and_gravitational_plotter()
