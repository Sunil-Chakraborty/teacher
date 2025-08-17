import re

# Input and output file paths
input_file = "WA.txt"
output_file = "WA_filtered1.txt"
target_number = "+91 79809 33948"

# Regular expression to detect new message lines
# Typical format: 02/03/2023, 14:16 - +91 79809 33948: Message
msg_pattern = re.compile(r"^\d{2}/\d{2}/\d{4}, \d{2}:\d{2} - ")

# Storage for current message
current_msg = ""
include_current = False

with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8") as outfile:
    for line in infile:
        if msg_pattern.match(line):
            # New message starting — write previous one if from target number
            if include_current and current_msg:
                outfile.write(current_msg.strip() + "\n\n")
            
            # Reset current message
            current_msg = line
            include_current = f"- {target_number}:" in line
        else:
            # Continuation of the current message
            current_msg += line

    # Write the last message if it qualifies
    if include_current and current_msg:
        outfile.write(current_msg.strip() + "\n\n")

print(f"All messages from {target_number} have been extracted to {output_file}.")
