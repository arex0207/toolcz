import re
from pathlib import Path

BASE = Path("/Users/chenzonghai/Desktop/toolcz")
FILES = [
    "video-translation.html",
    "lumacue.html",
    "speakloop.html",
    "qr-barcode-fast-scanner.html",
    "chat-backup-reader.html",
]

section_pattern = re.compile(
    r'(<div class="section"><h2>Policy And Support</h2>)([\s\S]*?)(</div>\s*</div>\s*</body>)'
)
icon_pattern = re.compile(r'<p class="support-x-line">[\s\S]*?</p>')

for filename in FILES:
    path = BASE / filename
    text = path.read_text(encoding="utf-8")

    match = section_pattern.search(text)
    if not match:
        print(f"section-miss: {filename}")
        continue

    head, body, tail = match.groups()
    icon_match = icon_pattern.search(body)
    if not icon_match:
        print(f"icon-miss: {filename}")
        continue

    icon_html = icon_match.group(0)
    body_no_icon = icon_pattern.sub("", body)

    paragraph_match = re.search(r"<p>([\s\S]*?)</p>", body_no_icon)
    if paragraph_match:
        text_html = paragraph_match.group(1).strip()
    else:
        paragraph_open = body_no_icon.find("<p>")
        paragraph_next = body_no_icon.find("<p", paragraph_open + 3)
        if paragraph_open != -1 and paragraph_next != -1:
            text_html = body_no_icon[paragraph_open + 3 : paragraph_next].strip()
        else:
            print(f"text-miss: {filename}")
            continue

    new_body = f"<p class=\"support-x-line\">{icon_html.split('<p class=\"support-x-line\">', 1)[1]}"
    new_body += f"<p>{text_html}</p>"

    new_section = head + new_body + tail
    text = text[: match.start()] + new_section + text[match.end() :]
    path.write_text(text, encoding="utf-8")
    print(f"updated: {filename}")
