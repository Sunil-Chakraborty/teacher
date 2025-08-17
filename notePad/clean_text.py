# clean up text .

import unicodedata
import re
from pathlib import Path

# Read original text
text = Path("test.txt").read_text(encoding="utf-8")

# 1. Normalize Unicode (NFKC merges some equivalent characters)
text = unicodedata.normalize("NFKC", text)

# 2. Remove zero-width characters, BOM, and control characters (except \n \t)
hidden_chars_pattern = r"[\u200B-\u200D\uFEFF\u2060-\u206F\u202A-\u202E]"
text = re.sub(hidden_chars_pattern, "", text)

# 3. Replace multiple spaces with single space
text = re.sub(r"[ \t]+", " ", text)

# 4. Normalize newlines to \n
text = text.replace("\r\n", "\n").replace("\r", "\n")

# 5. Remove leading/trailing spaces on each line
text = "\n".join(line.strip() for line in text.split("\n"))

# Save cleaned text
Path("Poem2_cleaned.txt").write_text(text, encoding="utf-8")

print("✅ Poem2_cleaned.txt generated successfully.")
