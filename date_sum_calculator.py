import streamlit as st
import pandas as pd
from datetime import datetime

def sum_of_day_digits_corrected(date):
    day = int(date.strftime('%d'))
    day_sum = (day % 10) + (day // 10)
    return day_sum if day_sum < 10 else (day_sum % 10) + (day_sum // 10)

def sum_of_digits_reduced(date):
    full_sum = sum(int(digit) for digit in date.strftime('%d%m%Y'))
    reduced_sum = full_sum % 9 if full_sum % 9 != 0 else 9
    return reduced_sum

def generate_date_sums(year, month):
    dates = pd.date_range(start=f"{year}-{month:02d}-01", end=f"{year}-{month:02d}-{pd.Period(year=year, month=month, freq='M').days_in_month}")
    data_corrected_final = []
    for date in dates:
        day_sum = sum_of_day_digits_corrected(date)
        reduced_sum = sum_of_digits_reduced(date)
        data_corrected_final.append([date.strftime('%d/%m/%Y'), day_sum, reduced_sum])
    df_corrected_final = pd.DataFrame(data_corrected_final, columns=['Date', 'D+D', 'D+D+M+M+Y+Y+Y+Y (Reduced to base 9)'])
    return df_corrected_final

def date_sum_calculator():
    st.header("Date Sum Calculator")
    year = st.number_input("Enter the year (e.g., 2024):", min_value=1900, max_value=2100, value=2024, step=1)
    month = st.number_input("Enter the month (1-12):", min_value=1, max_value=12, value=1, step=1)
    df_result = generate_date_sums(year, month)
    number_filter = st.number_input("Enter the number you want the list of (1-9):", min_value=1, max_value=9, value=1, step=1)
    filtered_df = df_result[(df_result['D+D'] == number_filter) | (df_result['D+D+M+M+Y+Y+Y+Y (Reduced to base 9)'] == number_filter)]
    st.dataframe(filtered_df)
    csv = filtered_df.to_csv(index=False)
    st.download_button(label="Download CSV", data=csv, file_name='date_sums.csv', mime='text/csv')
