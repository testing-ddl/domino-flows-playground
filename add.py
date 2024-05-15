def read_input(input_name):
    input_location = f"/workflow/inputs/{input_name}"
    with open(input_location, "r") as file:
        return file.read()

def write_output(output_name, content):
    output_location = f"/workflow/inputs{output_name}"
    with open(output_location, 'w') as file:
        file.write(content)

# Read inputs
a = int(read_input("first_value"))
b = int(read_input("second_value"))

# Calculate sum
sum = a + b
print(f"The sum of {a} + {b} is {sum}")

# Write output
write_output("sum", str(sum))
