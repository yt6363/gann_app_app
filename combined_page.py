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

def reduce_to_single_digit_dob(n):
    while n >= 10:
        n = sum_digits(n)
    return n

# Chaldean Numerology functions
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

# Pythagorean Numerology functions
def pythagorean_numerology(input_str):
    numerology_table = {
        'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9,
        'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 6, 'P': 7, 'Q': 8, 'R': 9,
        'S': 1, 'T': 2, 'U': 3, 'V': 4, 'W': 5, 'X': 6, 'Y': 7, 'Z': 8, ' ': 0,
        '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '0': 0
    }
    total_sum = 0
    for char in input_str.upper():
        if char in numerology_table:
            total_sum += numerology_table[char]
    reduced_sum = reduce_to_single_digit(total_sum)
    return reduced_sum

# DOB Analyzer functions
def analyze_dob(dob):
    day, month, year = dob.split('/')
    digits = [int(d) for part in (day, month, year) for d in part]
    d_plus_d = sum(int(d) for d in day)
    reduced_d_plus_d = reduce_to_single_digit_dob(d_plus_d)
    total_sum = sum(digits)
    reduced_total_sum = reduce_to_single_digit_dob(total_sum)
    digit_count = {str(d): 0 for d in range(1, 10)}
    for digit in digits:
        if digit != 0:
            digit_count[str(digit)] += 1
    present_digits = {k: v for k, v in digit_count.items() if v > 0}
    all_digits_base_9 = set(str(d) for d in range(1, 10))
    present_digits_set = set(present_digits.keys())
    missing_digits = sorted(all_digits_base_9 - present_digits_set)
    results = {
        "d+d": reduced_d_plus_d,
        "Total sum of all digits": reduced_total_sum,
        "List of all numbers present in the DOB": present_digits,
        "All the numbers not present in the base 9 number system": missing_digits
    }
    return results

def combined_numerology_and_dob_analyzer():
    st.title("Combined Numerology and Date of Birth Analyzer")

    # Initialize session state for history
    if "numerology_history" not in st.session_state:
        st.session_state.numerology_history = []

    # Numerology Input
    input_str = st.text_input("Enter a string for Numerology Calculation:")
    dob = st.text_input("Enter your date of birth (DD/MM/YYYY):")

    if st.button("Calculate"):
        if input_str:
            chaldean_result = chaldean_numerology(input_str)
            pythagorean_result = pythagorean_numerology(input_str)

            # Append results to the session history
            st.session_state.numerology_history.append({
                "Input": input_str,
                "Pythagorean": pythagorean_result,
                "Chaldean": chaldean_result
            })

        if dob:
            results = analyze_dob(dob)
            st.write(f"1) d+d = {results['d+d']}")
            st.write(f"2) Total sum of all digits = {results['Total sum of all digits']}")
            st.write(f"3) List of all numbers present in the DOB: {', '.join(f'{k}({v})' for k, v in results['List of all numbers present in the DOB'].items())}")
            st.write(f"4) All the numbers not present in the base 9 number system: {', '.join(results['All the numbers not present in the base 9 number system'])}")

            # Prepare results for download
            dob_results_df = pd.DataFrame({
                "Description": ["d+d", "Total sum of all digits", "List of all numbers present in the DOB", "All the numbers not present in the base 9 number system"],
                "Value": [results['d+d'], results['Total sum of all digits'], ', '.join(f'{k}({v})' for k, v in results['List of all numbers present in the DOB'].items()), ', '.join(results['All the numbers not present in the base 9 number system'])]
            })

            st.download_button(label="Download DOB Analysis CSV", data=dob_results_df.to_csv(index=False), file_name='dob_analysis.csv', mime='text/csv')

    # Display all results in a table
    if st.session_state.numerology_history:
        history_df = pd.DataFrame(st.session_state.numerology_history)
        st.table(history_df)

        # Provide a download button for all numerology results
        csv = history_df.to_csv(index=False)
        st.download_button(label="Download Numerology Results CSV", data=csv, file_name='numerology_results.csv', mime='text/csv')
