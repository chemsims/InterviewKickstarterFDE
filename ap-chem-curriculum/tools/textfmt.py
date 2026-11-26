"""Text helpers shared by the worksheet and lesson-plan builders.

Content files use plain Unicode chemistry text (H₂O, ΔH°, →, ⇌, 10⁻³).
Poppins has no glyphs for many of those, so every character Poppins lacks is
wrapped in a DejaVu Sans <font> tag, and Unicode sub/superscript digits are
turned into reportlab <sub>/<super> markup so they render at a sensible size.
"""
import html
import os
import re

from reportlab.pdfbase.ttfonts import TTFontFile

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "fonts")

_poppins_cmap = set(TTFontFile(os.path.join(FONT_DIR, "Poppins-Regular.ttf")).charToGlyph.keys())

SUB = {"₀": "0", "₁": "1", "₂": "2", "₃": "3", "₄": "4", "₅": "5", "₆": "6", "₇": "7", "₈": "8", "₉": "9",
       "₊": "+", "₋": "−", "ₙ": "n", "ₐ": "a", "ₑ": "e", "ₓ": "x", "ᵢ": "i", "ₚ": "p", "ₖ": "k", "ₘ": "m", "ₜ": "t", "ₛ": "s", "ₕ": "h", "ₗ": "l", "ᵥ": "v", "ᵣ": "r", "ₒ": "o"}
SUP = {"⁰": "0", "¹": "1", "²": "2", "³": "3", "⁴": "4", "⁵": "5", "⁶": "6", "⁷": "7", "⁸": "8", "⁹": "9",
       "⁺": "+", "⁻": "−", "ⁿ": "n", "°": None}  # ° stays as a glyph


def _font_fallback(s: str) -> str:
    out = []
    for ch in s:
        if ch in "<>&" or ord(ch) < 128 or ord(ch) in _poppins_cmap:
            out.append(ch)
        else:
            out.append(f'<font name="DejaVu">{ch}</font>')
    return "".join(out)


def _runs(s: str, table: dict, tag: str) -> str:
    keys = "".join(k for k, v in table.items() if v is not None)
    pat = re.compile(f"[{re.escape(keys)}]+")
    return pat.sub(lambda m: f"<{tag}>" + "".join(table[c] for c in m.group(0)) + f"</{tag}>", s)


def rich(text: str) -> str:
    """Plain content text -> reportlab paragraph markup.

    Supports **bold** and *italic* markdown-style emphasis. Everything else is
    escaped, so stray < or & in chemistry text can't break the paragraph.
    """
    if text is None:
        return ""
    s = html.escape(str(text), quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<i>\1</i>", s)
    s = _runs(s, SUB, "sub")
    s = _runs(s, SUP, "super")
    # fallback must not touch the tags we just made: split on tags
    parts = re.split(r"(<[^>]+>)", s)
    return "".join(p if p.startswith("<") else _font_fallback(p) for p in parts)
