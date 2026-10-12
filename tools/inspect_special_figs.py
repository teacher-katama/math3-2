import pymupdf
import os

targets = [
    ("選修數學乙(下)課本_01_編輯大意、目次.pdf", "01_toc"),
    ("選修數學乙(下)課本_03_CH1_學習活動.pdf", "03_ch1_act"),
    ("選修數學乙(下)課本_04_CH1_數學家小傳.pdf", "04_ch1_bio"),
    ("選修數學乙(下)課本_07_CH2_學習活動.pdf", "07_ch2_act"),
    ("選修數學乙(下)課本_08_CH2_綜合演練.pdf", "08_ch2_ex"),
    ("選修數學乙(下)課本_09_CH2_數學家小傳.pdf", "09_ch2_bio"),
    ("選修數學乙(下)課本_12_CH3_學習活動.pdf", "12_ch3_act"),
    ("選修數學乙(下)課本_13_CH3_綜合演練.pdf", "13_ch3_ex"),
    ("選修數學乙(下)課本_17_習題參考解答.pdf", "15_sol_ex"),
]

for f, prefix in targets:
    doc = pymupdf.open(f)
    print(f"\n*** {f} ***")
    for pno, p in enumerate(doc):
        imgs = p.get_images()
        draws = p.get_drawings()
        print(f"  Page {pno+1}: {len(imgs)} imgs, {len(draws)} draws")
        # Let's inspect where drawings are clustered or where images are placed
        for img in imgs:
            xref = img[0]
            # find bbox of image on page
            rects = p.get_image_rects(xref)
            print(f"    img xref={xref}, rects={rects}")
