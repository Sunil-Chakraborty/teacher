from pydub import AudioSegment, effects
import os

# Input and output file paths
input_path = "audio1.m4a"
output_path = "audio1.mp3"

# Load audio
audio = AudioSegment.from_file(input_path, format="m4a")

# Normalize volume
normalized_audio = effects.normalize(audio)

# Apply a simple high-pass filter to remove low-frequency rumble
filtered_audio = normalized_audio.high_pass_filter(80)

# Apply a low-pass filter to remove extreme high-frequency noise
filtered_audio = filtered_audio.low_pass_filter(8000)

# Export enhanced audio
filtered_audio.export(output_path, format="mp3")

output_path
