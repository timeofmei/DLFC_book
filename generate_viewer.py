from pathlib import Path
import json
import re

OUTPUT_FILE = Path("index.html")
SVG_DIR = Path("svg")

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
        #controls {{
            position: fixed;
            left: 12px;
            bottom: 12px;
            background: rgba(0, 0, 0, 0.75);
            color: #fff;
            padding: 8px 10px;
            border-radius: 6px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4);
            z-index: 10;
            font-size: 14px;
            transition: opacity 0.25s ease, transform 0.25s ease;
        }}
        #controls.controls-hidden {{
            opacity: 0;
            transform: translateY(6px);
        }}
        #chapterSelect {{
            padding: 4px 6px;
            border-radius: 4px;
            border: none;
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
    <div id="controls">
        <select id="chapterSelect">
            {chapter_options}
        </select>
    </div>
    <div id="pages" class="container"></div>
    <script>
        const CHAPTERS = {chapters_json};

        const container = document.getElementById("pages");
        const select = document.getElementById("chapterSelect");
        const controls = document.getElementById("controls");
        let hideTimer = null;

        function clearImages() {{
            const imgs = container.querySelectorAll("img");
            imgs.forEach((img) => {{
                img.removeAttribute("src");
            }});
            container.innerHTML = "";
        }}

        function renderChapter(chapterId) {{
            clearImages();
            const pages = CHAPTERS[chapterId] || [];
            const cacheBust = Date.now();
            const fragment = document.createDocumentFragment();

            pages.forEach((pageNum) => {{
                const wrapper = document.createElement("div");
                wrapper.className = "page-wrapper";

                const img = document.createElement("img");
                img.alt = `Page ${{pageNum}}`;
                img.loading = "lazy";
                img.src = `svg/${{chapterId}}/page_${{pageNum}}.svg?cb=${{cacheBust}}`;

                wrapper.appendChild(img);
                fragment.appendChild(wrapper);
            }});

            container.appendChild(fragment);
        }}

        select.addEventListener("change", (event) => {{
            renderChapter(event.target.value);
        }});

        if (select.value) {{
            renderChapter(select.value);
        }}

        function scheduleHide() {{
            if (hideTimer) {{
                clearTimeout(hideTimer);
            }}
            hideTimer = setTimeout(() => {{
                controls.classList.add("controls-hidden");
            }}, 2000);
        }}

        scheduleHide();
        controls.addEventListener("mouseenter", () => {{
            controls.classList.remove("controls-hidden");
            if (hideTimer) {{
                clearTimeout(hideTimer);
                hideTimer = null;
            }}
        }});
        controls.addEventListener("mouseleave", () => {{
            scheduleHide();
        }});
    </script>
</body>
</html>
"""


def build_chapters():
    chapters = {}
    for entry in SVG_DIR.iterdir():
        if not entry.is_dir():
            continue
        if not re.fullmatch(r"c\d+", entry.name):
            continue
        pages = []
        for svg in entry.glob("page_*.svg"):
            match = re.search(r"page_(\d+)\.svg", svg.name)
            if match:
                pages.append(int(match.group(1)))
        pages.sort()
        if pages:
            chapters[entry.name] = pages

    def chapter_key(name):
        return int(name[1:])

    return dict(sorted(chapters.items(), key=lambda item: chapter_key(item[0])))


def generate_html():
    chapters = build_chapters()
    chapter_options = []
    for idx, chapter_id in enumerate(chapters.keys()):
        chapter_num = chapter_id[1:]
        if chapter_num == "0":
            label = "Preface"
        elif chapter_num == "21":
            label = "Appendix"
        elif chapter_num == "22":
            label = "Bib & Index"
        else:
            label = f"Chapter {chapter_num}"
        selected = " selected" if idx == 0 else ""
        chapter_options.append(
            f'<option value="{chapter_id}"{selected}>{label}</option>'
        )

    html_content = HTML_TEMPLATE.format(
        chapter_options="\n            ".join(chapter_options),
        chapters_json=json.dumps(chapters)
    )

    OUTPUT_FILE.write_text(html_content, encoding="utf-8")
    print(f"Generated {OUTPUT_FILE} with {len(chapters)} chapters.")


if __name__ == "__main__":
    generate_html()
