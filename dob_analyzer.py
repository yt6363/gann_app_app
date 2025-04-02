import streamlit as st
import pandas as pd

def sum_digits(n):
    return sum(int(d) for d in str(n))

def reduce_to_single_digit_dob(n):
    while n >= 10:
        n = sum_digits(n)
    return n

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

def dob_analyzer():
    st.header("Date of Birth Analyzer")
    dob = st.text_input("Enter your date of birth (DD/MM/YYYY):")
    if st.button("Analyze DOB"):
        if dob:
            results = analyze_dob(dob)
            st.write(f"1) d+d = {results['d+d']}")
            st.write(f"2) Total sum of all digits = {results['Total sum of all digits']}")
            st.write(f"3) List of all numbers present in the DOB: {', '.join(f'{k}({v}^)' for k, v in results['List of all numbers present in the DOB'].items())}")
            st.write(f"4) All the numbers not present in the base 9 number system: {', '.join(results['All the numbers not present in the base 9 number system'])}")
            results_df = pd.DataFrame({
                "Description": ["d+d", "Total sum of all digits", "List of all numbers present in the DOB", "All the numbers not present in the base 9 number system"],
                "Value": [results['d+d'], results['Total sum of all digits'], ', '.join(f'{k}({v}^)' for k, v in results['List of all numbers present in the DOB'].items()), ', '.join(results['All the numbers not present in the base 9 number system'])]
            })
            csv = results_df.to_csv(index=False)
            st.download_button(label="Download CSV", data=csv, file_name='dob_analysis.csv', mime='text/csv')
