from pathlib import Path

TOTAL_PAGES = 666
OUTPUT_FILE = Path("index.html")

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Deep Learning: Foundations and Concepts</title>
    <style>
        body {{
            background-color: #333; /* Darker background for better contrast */
            margin: 0;
            padding: 0;
            font-family: sans-serif;
            display: flex;
            justify-content: center;
        }}
        .container {{
            width: 100%;
            max-width: 1000px; /* Adaptive max width */
            padding: 20px 10px;
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
            gap: 20px;
        }}
        .page-wrapper {{
            width: 100%;
            background-color: white;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
            border-radius: 4px;
            overflow: hidden; /* Crop the scaled image */
            position: relative;
            /* Maintain aspect ratio or let content dictate height */
        }}
        img {{
            display: block;
            width: 100%;
            height: auto;
            transform: scale(1.2); /* Scale to 120% */
            transform-origin: center center;
        }}
    </style>
</head>
<body>
    <div class="container">
        {images}
    </div>
</body>
</html>
"""


def generate_html():
    images = []
    for i in range(1, TOTAL_PAGES + 1):
        # Wrap image in a div for overflow hidden
        img_block = f'<div class="page-wrapper"><img src="svg/page_{i}.svg" alt="Page {i}" loading="lazy"></div>'
        images.append(img_block)

    html_content = HTML_TEMPLATE.format(images="\n        ".join(images))

    OUTPUT_FILE.write_text(html_content, encoding="utf-8")
    print(f"Generated {OUTPUT_FILE} with {TOTAL_PAGES} images.")


if __name__ == "__main__":
    generate_html()
