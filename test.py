# Global array
my_array = [1, 2, 3]

def modify_array():
    # No need for the `global` keyword when modifying the contents
    my_array[2]=5
    print(f"Inside function: {my_array}")

# Call the function
modify_array()

# Check the global array
print(f"Outside function: {my_array}")
