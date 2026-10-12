import pymupdf
import glob
import os

os.makedirs("tools/texts", exist_ok=True)

files = sorted(glob.glob("*.pdf"))
for f in files:
    doc = pymupdf.open(f)
    base = os.path.splitext(f)[0]
    out_file = f"tools/texts/{base}.txt"
    with open(out_file, "w", encoding="utf-8") as out:
        for pno, p in enumerate(doc):
            out.write(f"\n===== [PAGE {pno+1}] =====\n")
            out.write(p.get_text())
    print(f"Dumped {base}.txt ({len(doc)} pages)")
