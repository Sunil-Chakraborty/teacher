
# file:///D:/JU/index.html
# python generate_poem_html.py


import re
from pathlib import Path

# Read the poem file
with open("Poem.txt", "r", encoding="utf-8") as f:
    raw_text = f.read()

# Extract poems sent by +91 79809 33948
pattern = re.compile(
    r"(\d{2}/\d{2}/\d{4}, \d{2}:\d{2}) - \+91 79809 33948: [\"']{0,2}(.*?)[\"']{0,2}\n\n(.*?)(?=\n\d{2}/\d{2}/\d{4}, \d{2}:\d{2} - |\Z)",
    re.DOTALL
)
matches = pattern.findall(raw_text)

# Create the HTML content
html = """<!DOCTYPE html>
<html lang="bn">
<head>
  <meta charset="UTF-8">
  <title>বাংলা কবিতা সংকলন</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body { font-family: 'Noto Serif Bengali', serif; margin: 0; padding: 0; display: flex; height: 100vh; overflow: hidden; }
    aside { width: 30%; background: #f4f4f4; padding: 2em; overflow-y: auto; border-right: 1px solid #ccc; }
    main { width: 70%; padding: 2em; overflow-y: auto; }
    h1 { color: #003366; margin-top: 0; }
    .index a { display: block; margin: 0.5em 0; color: #0066cc; text-decoration: none; }
    .index a:hover { text-decoration: underline; }
    .poem { margin-bottom: 4em; }
    p { white-space: pre-line; }
  </style>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+Bengali&display=swap" rel="stylesheet">
</head>
<body>
  <aside>
    <h1>📚 বাংলা কবিতা সংকলন</h1>
    <p><strong>✍ কবি : অধীর মন্ডল (+91 79809 33948)</strong></p>
    <div class="index">
"""

# Add index links and poem content
main_content = ""
for idx, (_, title, body) in enumerate(matches, start=1):
    anchor = f"poem{idx}"
    html += f'      <a href="#{anchor}">{title}</a>\n'
    main_content += f"""
    <div class="poem" id="{anchor}">
      <h2>{title}</h2>
      <p>{body.strip()}</p>
    </div>
"""

# Finish the HTML
html += f"""    </div>
  </aside>
  <main>
{main_content}
  </main>
</body>
</html>
"""

# Save to file
Path("index.html").write_text(html, encoding="utf-8")
print("✅ index.html has been generated successfully!")
