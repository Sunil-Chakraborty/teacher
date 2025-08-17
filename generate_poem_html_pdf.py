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

# Begin HTML content
html = """<!DOCTYPE html>
<html lang="bn">
<head>
  <meta charset="UTF-8">
  <title>বাংলা কবিতা সংকলন</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body {
      font-family: 'Noto Serif Bengali', serif;
      margin: 0;
      padding: 20px;
    }
    header {
      margin-bottom: 20px;
    }
    h1 {
      color: #003366;
    }
    .index a {
      display: block;
      margin: 0.3em 0;
      color: #0066cc;
      text-decoration: none;
    }
    .index a:hover {
      text-decoration: underline;
    }
    .poem {
      margin-bottom: 40px;
    }
    p {
      white-space: pre-line;
    }
    button {
      background-color: #007bff;
      color: white;
      padding: 10px 15px;
      border: none;
      cursor: pointer;
      margin-bottom: 20px;
    }
    button:hover {
      background-color: #0056b3;
    }
    @media print {
      button, .index { display: none; }
    }
  </style>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+Bengali&display=swap" rel="stylesheet">
</head>
<body>
  <header>
    <h1>📚 বাংলা কবিতা সংকলন</h1>
    <p><strong>✍ কবি : অধীর মন্ডল (+91 79809 33948)</strong></p>
  </header>

  <button onclick="downloadPDF()">📄 Download All Poems as PDF</button>

  <div class="index">
"""

# Build index and content
poem_content = '<div id="poems">\n'

for idx, (_, title, body) in enumerate(matches, start=1):
    anchor = f"poem{idx}"
    html += f'    <a href="#{anchor}">{title}</a>\n'
    poem_content += f"""
  <div class="poem" id="{anchor}">
    <h2>{title}</h2>
    <p>{body.strip()}</p>
  </div>
"""

poem_content += '</div>'

# Finish HTML
html += f"""  </div>
{poem_content}
  <script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>
  <script>
    function downloadPDF() {{
      const element = document.getElementById("poems");
      const opt = {{
        margin: 0.5,
        filename: 'bangla_poems.pdf',
        image: {{ type: 'jpeg', quality: 0.98 }},
        html2canvas: {{ scale: 2 }},
        jsPDF: {{ unit: 'in', format: 'a4', orientation: 'portrait' }}
      }};
      html2pdf().set(opt).from(element).save();
    }}
  </script>
</body>
</html>
"""

# Save file
Path("index1.html").write_text(html, encoding="utf-8")
print("✅ index1.html has been generated successfully with working Bengali PDF export!")
