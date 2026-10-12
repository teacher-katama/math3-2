import pymupdf
import re
import os
import glob

os.makedirs("images", exist_ok=True)

def clean_name(s):
    return re.sub(r'[^\w\-_.]', '_', s)

file_prefixes = {
    "選修數學乙(下)課本_01_編輯大意、目次.pdf": "01_toc",
    "選修數學乙(下)課本_02_CH1_線性規劃.pdf": "02_ch1",
    "選修數學乙(下)課本_03_CH1_學習活動.pdf": "03_ch1_act",
    "選修數學乙(下)課本_04_CH1_數學家小傳.pdf": "04_ch1_bio",
    "選修數學乙(下)課本_05_CH2-1_複數.pdf": "05_ch2_1",
    "選修數學乙(下)課本_06_CH2-2_多項式方程式.pdf": "06_ch2_2",
    "選修數學乙(下)課本_07_CH2_學習活動.pdf": "07_ch2_act",
    "選修數學乙(下)課本_08_CH2_綜合演練.pdf": "08_ch2_ex",
    "選修數學乙(下)課本_09_CH2_數學家小傳.pdf": "09_ch2_bio",
    "選修數學乙(下)課本_10_CH3-1_離散型隨機變數.pdf": "10_ch3_1",
    "選修數學乙(下)課本_11_CH3-2_二項分布.pdf": "11_ch3_2",
    "選修數學乙(下)課本_12_CH3_學習活動.pdf": "12_ch3_act",
    "選修數學乙(下)課本_13_CH3_綜合演練.pdf": "13_ch3_ex",
    "選修數學乙(下)課本_16_隨堂練習參考解答.pdf": "14_sol_practice",
    "選修數學乙(下)課本_17_習題參考解答.pdf": "15_sol_ex",
}

extracted_count = 0

for pdf_file, prefix in sorted(file_prefixes.items()):
    if not os.path.exists(pdf_file):
        continue
    doc = pymupdf.open(pdf_file)
    print(f"\nProcessing {pdf_file} ({len(doc)} pages)...")
    
    for pno, page in enumerate(doc):
        blocks = page.get_text("blocks")
        drawings = page.get_drawings()
        
        # 1. Look for Figure captions: 圖 X
        found_figs = []
        for b in blocks:
            text = b[4].strip()
            # check lines
            for line in text.split("\n"):
                m = re.fullmatch(r"圖\s*(\d+[a-z]?)", line.strip())
                if m:
                    found_figs.append((m.group(0).replace(" ", ""), b[:4]))
        
        # Process each captioned figure
        for fig_label, caption_box in found_figs:
            cx0, cy0, cx1, cy1 = caption_box
            # Define search zone above caption
            # In typical layout, figure is strictly above caption within 180pt, horizontal within +/- 120pt
            search_rect = pymupdf.Rect(cx0 - 130, cy0 - 200, cx1 + 130, cy1)
            
            # Find drawings
            fig_rect = pymupdf.Rect(caption_box)
            has_drawings = False
            for d in drawings:
                dr = pymupdf.Rect(d["rect"])
                if search_rect.contains(dr) and dr.width < 320 and dr.height < 250:
                    fig_rect.include_rect(dr)
                    has_drawings = True
            
            # Find small text labels inside
            for tb in blocks:
                tbr = pymupdf.Rect(tb[:4])
                txt = tb[4].strip()
                if search_rect.contains(tbr) and len(txt) <= 25 and not re.match(r"^\d+$", txt):
                    if tbr.y1 <= cy1:
                        fig_rect.include_rect(tbr)
            
            # Ensure top does not overlap text paragraph above
            # Check paragraph blocks directly above fig_rect
            top_bound = 0
            for tb in blocks:
                tbr = pymupdf.Rect(tb[:4])
                txt = tb[4].strip()
                if len(txt) > 25: # actual paragraph
                    if tbr.x0 < fig_rect.x1 and tbr.x1 > fig_rect.x0 and tbr.y1 <= fig_rect.y0 + 10:
                        top_bound = max(top_bound, tbr.y1)
            
            y_start = max(fig_rect.y0 - 5, top_bound + 2)
            crop_box = pymupdf.Rect(fig_rect.x0 - 6, y_start, fig_rect.x1 + 6, cy1 + 6)
            
            # Ensure valid dimensions
            if crop_box.width > 20 and crop_box.height > 20:
                pix = page.get_pixmap(clip=crop_box, dpi=200)
                out_name = f"images/{prefix}_p{pno+1}_{fig_label}.png"
                pix.save(out_name)
                print(f"  Saved figure: {out_name} ({pix.width}x{pix.height})")
                extracted_count += 1

print(f"\nTotal figures extracted: {extracted_count}")
