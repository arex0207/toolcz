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

pattern = re.compile(
    r"(<h2>Policy And Support</h2>)(\s*)"
    r"(<p class=\"support-x-line\">[\s\S]*?</p>)(\s*)"
    r"(<p>[\s\S]*?</p>)"
)

for filename in FILES:
    path = BASE / filename
    text = path.read_text(encoding="utf-8")
    new_text, count = pattern.subn(r"\1\2\5\4\3", text, count=1)
    if count:
        path.write_text(new_text, encoding="utf-8")
        print(f"updated: {filename}")
    else:
        print(f"no-change: {filename}")
