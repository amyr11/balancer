import streamlit as st
from collections import defaultdict


def find_first_sum_combination(nums, target):
    nums = [
        num for num in nums if num <= target
    ]  # Ignore numbers larger than the target
    nums.sort()  # Sorting helps with early termination
    result = []
    seen = set()

    def backtrack(start, target, path):
        if target == 0:
            path_tuple = tuple(sorted(path))  # Sorting to avoid duplicates
            if path_tuple not in seen:
                result.append(path[:])
                seen.add(path_tuple)
            return True  # Stop at first valid combination
        if target < 0:
            return False

        for i in range(start, len(nums)):
            if nums[i] > target:  # Early termination condition
                break
            if i > start and nums[i] == nums[i - 1]:  # Skip duplicates
                continue
            path.append(nums[i])
            if backtrack(i + 1, target - nums[i], path):  # Stop early
                return True
            path.pop()

        return False

    backtrack(0, target, [])
    return result[0] if result else None  # Return only the first valid combination


def balancer(*arrays, target):
    combined = []
    index_map = defaultdict(list)  # Store all occurrences of a number
    for i, arr in enumerate(arrays):
        for num in arr:
            if num <= target:  # Ignore numbers larger than the target
                combined.append(num)
                index_map[num].append(i + 1)  # Track all sources

    result = find_first_sum_combination(combined, target)

    if result:
        grouped = defaultdict(list)
        used_counts = defaultdict(int)  # Track used instances of numbers

        for num in result:
            source_list = index_map[num][
                used_counts[num] % len(index_map[num])
            ]  # Cycle through sources
            grouped[source_list].append(num)
            used_counts[num] += 1

        return grouped
    return None


st.title("Combination Finder")

num_arrays = st.number_input("Enter number of arrays", min_value=1, value=2, step=1)
arrays = []
for i in range(num_arrays):
    arr_input = st.text_area(f"Enter list {i+1} (comma-separated numbers)", "")
    try:
        arr = list(map(float, arr_input.split(","))) if arr_input else []
        arrays.append(arr)
    except ValueError:
        st.error(f"Invalid input in list {i+1}. Please enter valid numbers.")

target_input = st.number_input("Enter target sum")

if st.button("Find Combination"):
    result = balancer(*arrays, target=target_input)

    if result:
        st.success("Combination found:")
        total_sum = 0
        for source, nums in sorted(result.items()):
            st.header(f"From list {source}")
            for num in nums:
                st.text(f"{num}")
                total_sum += num
            st.text("")  # Space between lists

        st.write("------------")
        st.text(f"Total: {total_sum}")
    else:
        st.error("No combination found")
