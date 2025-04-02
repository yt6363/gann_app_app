import streamlit as st
import pandas as pd

def sum_digits(n):
    return sum(int(d) for d in str(n))

def reduce_to_single_digit(n):
    if n in {11, 22, 33}:
        return n
    while n >= 10:
        n = sum_digits(n)
        if n in {11, 22, 33}:
            return n
    return n

def chaldean_numerology(input_str):
    numerology_table = {
        'A': 1, 'I': 1, 'J': 1, 'Q': 1, 'Y': 1,
        'B': 2, 'K': 2, 'R': 2,
        'C': 3, 'G': 3, 'L': 3, 'S': 3,
        'D': 4, 'M': 4, 'T': 4,
        'E': 5, 'H': 5, 'N': 5, 'X': 5,
        'U': 6, 'V': 6, 'W': 6,
        'O': 7, 'Z': 7,
        'F': 8, 'P': 8
    }
    total_sum = 0
    for char in input_str.upper():
        if char in numerology_table:
            total_sum += numerology_table[char]
    reduced_sum = reduce_to_single_digit(total_sum)
    return reduced_sum

def chaldean_numerology_calculator():
    st.header("Chaldean Numerology Calculator")
    if "chaldean_history" not in st.session_state:
        st.session_state.chaldean_history = []
    input_str = st.text_input("Enter a string:")
    if st.button("Calculate Chaldean Numerology"):
        if input_str:
            result = chaldean_numerology(input_str)
            st.session_state.chaldean_history.append((input_str, result))
            st.write(f"The numerology value for '{input_str}' is: {result}")
    if st.session_state.chaldean_history:
        st.write("Previous Outputs:")
        for i, (inp, res) in enumerate(st.session_state.chaldean_history, 1):
            st.write(f"{i}. The numerology value for '{inp}' is: {res}")
        history_df = pd.DataFrame(st.session_state.chaldean_history, columns=['Input', 'Numerology Value'])
        csv = history_df.to_csv(index=False)
        st.download_button(label="Download CSV", data=csv, file_name='chaldean_numerology_history.csv', mime='text/csv')
