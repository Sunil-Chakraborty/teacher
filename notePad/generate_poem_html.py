# file:///D:/JU/index.html
# python generate_poem_html.py
import re
from pathlib import Path

with open("Poem3.txt", "r", encoding="utf-8") as f:
    raw_text = f.read()

# Regex: generic – capture poet + title + optional media
pattern = re.compile(
    r"(\d{2}/\d{2}/\d{4}, \d{2}:\d{2}) - (.*?): ?[\"']?(.*?)[\"']?\n"
    r"(?:(audio|video|image):(.*?)\n)?"  
    r"\n?(.*?)(?=\n\d{2}/\d{2}/\d{4}, \d{2}:\d{2} - |\Z)", 
    re.DOTALL
)
matches = pattern.findall(raw_text)

# Start HTML
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
    audio, video, img { margin-top: 10px; display: block; max-width: 100%; }
    video { max-height: 300px; }
  </style>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+Bengali&display=swap" rel="stylesheet">
</head>
<body>
  <aside>
    <h1>📚 বাংলা কবিতা সংকলন</h1>
    <div class="index">
"""

# Add poems
main_content = ""
for idx, (_, poet, title, media_type, media_file, body) in enumerate(matches, start=1):
    anchor = f"poem{idx}"
    html += f'      <a href="#{anchor}">{title}</a>\n'

    # Media check
    media_html = ""
    if media_file and media_file.strip():
        media_path = Path("media") / media_file.strip()
        if media_path.exists():
            if media_type == "audio":
                media_html = f'<audio controls><source src="media/{media_file.strip()}" type="audio/mpeg"></audio>'
            elif media_type == "video":
                media_html = f'<video controls><source src="media/{media_file.strip()}" type="video/mp4"></video>'
            elif media_type == "image":
                media_html = f'<img src="media/{media_file.strip()}" alt="{title}">'
        else:
            print(f"⚠️ Skipped missing media file: {media_file.strip()}")

    # Poem block with poet line (bold + italic)
    main_content += f"""
    <div class="poem" id="{anchor}">
      <h2>{title}</h2>
      <p><strong><em>কবি : {poet}</em></strong></p>
      {media_html}
      <p>{body.strip()}</p>
    </div>
"""

# Close aside + main
html += f"""    </div>
  </aside>
  <main id="poemContainer">
{main_content}
  </main>
</body>
</html>
"""

Path("index.html").write_text(html, encoding="utf-8")
print("✅ index.html generated successfully (কবি line bold + italic)!")
