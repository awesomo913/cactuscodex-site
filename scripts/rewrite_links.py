"""One-time rewrite of links after moving the codex from revolutionarydesigns.io/cactus/ to cactuscodex.org/."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEXT_EXT = {".html", ".js", ".css", ".xml", ".txt", ".json", ".md"}

LITERAL = [
    ("https://revolutionarydesigns.io/cactus/", "https://cactuscodex.org/"),
    ("https://revolutionarydesigns.io/gritty-mix/", "https://cactuscodex.org/gritty-mix/"),
    ("https://revolutionarydesigns.io/favicon.png", "https://cactuscodex.org/favicon.png"),
    ("https://revolutionarydesigns.io/assets/", "https://cactuscodex.org/assets/"),
    ('class="codex-wordmark" href="/">Revolutionary Designs</a>', 'class="codex-wordmark" href="/">Cactus Codex</a>'),
    ('href="/projects/">Projects</a>', 'href="https://revolutionarydesigns.io/">Revolutionary Designs</a>'),
    ('href="/game/"', 'href="https://revolutionarydesigns.io/game/"'),
]
# Root-relative "/cactus/..." paths become root paths on the new domain.
CACTUS_PATH = re.compile(r"""(["'(=])/cactus/""")
NAV_LABEL = [
    ('<a class="current" href="/">Cactus Codex</a>', '<a class="current" href="/">Field guide</a>'),
    ('<div><a href="/">Cactus Codex</a>', '<div><a href="/">Field guide</a>'),
]


def rewrite(text: str) -> str:
    for old, new in LITERAL:
        text = text.replace(old, new)
    text = CACTUS_PATH.sub(r"\1/", text)
    for old, new in NAV_LABEL:
        text = text.replace(old, new)
    return text


def main() -> int:
    changed = 0
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_EXT or "scripts" in path.parts:
            continue
        original = path.read_text(encoding="utf-8")
        updated = rewrite(original)
        if updated != original:
            path.write_text(updated, encoding="utf-8", newline="")
            changed += 1
    print(f"rewrote {changed} files")
    leftovers = [
        f"{p.relative_to(ROOT)}: {m.group(0)}"
        for p in ROOT.rglob("*")
        if p.is_file() and p.suffix.lower() in TEXT_EXT and "scripts" not in p.parts
        for m in re.finditer(r"revolutionarydesigns\.io/(cactus|gritty-mix)[^\s\"')]*|[\"'(=]/cactus/", p.read_text(encoding="utf-8"))
    ]
    print(f"leftover old-path references: {len(leftovers)}")
    for line in leftovers[:20]:
        print("  ", line)
    return 1 if leftovers else 0


if __name__ == "__main__":
    sys.exit(main())
