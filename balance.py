import streamlit as st
from itertools import combinations

def find_combinations(arr, target):
    for r in range(1, len(arr) + 1):
        for combo in combinations(arr, r):
            if sum(combo) == target:
                return list(combo)
    return None

def balancer(*arrays, target):
    combined = []
    index_map = {}
    for i, arr in enumerate(arrays):
        for num in arr:
            combined.append(num)
            index_map[num] = i + 1  # Store the array index (1-based)
    
    result = find_combinations(combined, target)
    
    if result:
        result_with_sources = [(num, index_map[num]) for num in result]
        return result_with_sources
    return None

st.title("Combination Finder")

num_arrays = st.number_input("Enter number of arrays", min_value=1, value=2, step=1)
arrays = []
for i in range(num_arrays):
    arr_input = st.text_area(f"Enter list {i+1} (comma-separated numbers)", "")
    try:
        arr = list(map(float, arr_input.split(','))) if arr_input else []
        arrays.append(arr)
    except ValueError:
        st.error(f"Invalid input in list {i+1}. Please enter valid numbers.")

target_input = st.number_input("Enter target sum", value=789770.65)

if st.button("Find Combination"):
    result = balancer(*arrays, target=target_input)
    
    if result:
        st.success("Combination found:")
        for num, source in result:
            st.write(f"{num} (from list {source})")
        st.write(f"Sum of combination: {sum(num for num, _ in result)}")
    else:
        st.error("No combination found")
