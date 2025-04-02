import streamlit as st

def calculate_price_at_degree(degree, stock_price):
    nearest_multiple = (stock_price // 360) * 360
    price_at_degree = nearest_multiple + degree
    return nearest_multiple, price_at_degree

def stock_price_at_degree():
    st.header("Stock Price at Degree Calculator")
    degree = st.number_input("Enter the degree (0 to 360):", min_value=0.0, max_value=360.0, step=1.0)
    stock_price = st.number_input("Enter the current stock price:", min_value=0.0, step=0.01)
    if st.button("Calculate Price at Degree"):
        cycle_start, price_at_degree = calculate_price_at_degree(degree, stock_price)
        st.write(f"The stock price falls in the cycle starting at {cycle_start}.")
        st.write(f"The stock price for {degree} degrees in this cycle is: {price_at_degree:.2f}")

def calculate_degrees(stock_price):
    nearest_multiple = (stock_price // 360) * 360
    difference = stock_price - nearest_multiple
    degrees = difference
    return degrees

def degrees_from_stock_price():
    st.header("Degrees from Stock Price Calculator")
    stock_price = st.number_input("Enter the stock price:", min_value=0.0, step=0.01)
    if st.button("Calculate Degrees"):
        degrees = calculate_degrees(stock_price)
        st.write(f"The degrees for the stock price {stock_price} is: {degrees:.2f}")
