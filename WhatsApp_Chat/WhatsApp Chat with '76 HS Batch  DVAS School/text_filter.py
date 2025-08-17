# Define input/output file paths
input_file = "WA.txt"
output_file = "WA_filtered.txt"
target_number = "+91 79809 33948"

with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8") as outfile:
    for line in infile:
        if f"- {target_number}:" in line:
            outfile.write(line)

print(f"Filtered messages saved to {output_file}")
