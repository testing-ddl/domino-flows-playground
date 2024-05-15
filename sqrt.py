def read_input(input_name):
    input_location = f"/workflow/inputs/{input_name}"
    with open(input_location, "r") as file:
        return file.read()

def write_output(output_name, content):
    output_location = f"/workflow/inputs{output_name}"
    with open(output_location, 'w') as file:
        file.write(content)

# Read inputs
value = int(read_input("value"))

# Calculate square root
sqrt = value ** 0.5
print(f"The square root of {value} is {sqrt}")

# Write output
write_output("sqrt", str(sqrt))
