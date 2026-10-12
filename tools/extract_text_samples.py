import pymupdf
import sys

def get_text(pdf_path):
    doc = pymupdf.open(pdf_path)
    res = []
    for i, p in enumerate(doc):
        res.append(f"--- PAGE {i+1} ---")
        res.append(p.get_text())
    return "\n".join(res)

with open("tools/out_01.txt", "w", encoding="utf-8") as f:
    f.write(get_text("選修數學乙(下)課本_01_編輯大意、目次.pdf"))

with open("tools/out_04.txt", "w", encoding="utf-8") as f:
    f.write(get_text("選修數學乙(下)課本_04_CH1_數學家小傳.pdf"))

with open("tools/out_03.txt", "w", encoding="utf-8") as f:
    f.write(get_text("選修數學乙(下)課本_03_CH1_學習活動.pdf"))

print("Extracted text for 01, 04, 03")
