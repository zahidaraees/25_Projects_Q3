'''
A web interface for inputting a sorted list and a target number

Real-time binary search with output

Streamlit-powered display for easy  to use
'''
import streamlit as st

def binary_search(arr, target):
    """
    Perform binary search on a sorted list.
    
    Parameters:
    arr (list): Sorted list of integers
    target (int): Target number to find
    
    Returns:
    int: Index of target if found, else -1
    """
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2
        st.write(f"Checking middle index {mid}, value: {arr[mid]}")
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1

# Streamlit App
st.title("🔍 Binary Search Web App")
st.write("This app performs a binary search on a sorted list using the divide and conquer approach.")

# Input from user
input_list = st.text_input("Enter a sorted list of integers (comma-separated):", "1, 3, 5, 7, 9, 11")
target = st.text_input("Enter the number to search for:", "7")

if st.button("Search"):
    try:
        arr = list(map(int, input_list.split(',')))
        arr.sort()  # Ensure the list is sorted
        target = int(target)
        st.write(f"Sorted list: {arr}")
        result = binary_search(arr, target)

        if result != -1:
            st.success(f"✅ Number {target} found at index {result}.")
        else:
            st.error(f"❌ Number {target} not found in the list.")
    except ValueError:
        st.error("Please enter valid integers separated by commas.")

