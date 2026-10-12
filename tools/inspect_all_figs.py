import pymupdf
import re
import glob

files = sorted(glob.glob("*.pdf"))

for f in files:
    doc = pymupdf.open(f)
    print(f"==================================================")
    print(f"FILE: {f} ({len(doc)} pages)")
    print(f"==================================================")
    for pno, p in enumerate(doc):
        # search for captions
        blocks = p.get_text("blocks")
        fig_captions = []
        for b in blocks:
            text = b[4].strip()
            # match lines like 圖 1, 圖 1a, 圖 20 等
            lines = text.split("\n")
            for line in lines:
                line_clean = line.strip()
                if re.fullmatch(r"圖\s*\d+[a-z]?", line_clean) or re.fullmatch(r"表\s*\d+", line_clean):
                    fig_captions.append((line_clean, b[:4]))
        
        drawings = p.get_drawings()
        images = p.get_images()
        if fig_captions or (len(images) > 0 and len(doc) <= 5):
            print(f"  Page {pno+1}: captions={fig_captions}, imgs={len(images)}, draws={len(drawings)}")
