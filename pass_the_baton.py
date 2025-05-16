from pathlib import Path

# Read inputs
a = Path("/workflow/inputs/input_value").read_text()

# Output the same number that was the input
number = int(a)
print(f"Passing the baton for number {a}")

# Write output
Path("/workflow/outputs/output_value").write_text(str(number))