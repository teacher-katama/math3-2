import pymupdf

def crop_and_save(pdf_path, page_idx, rect, out_path, dpi=200):
    doc = pymupdf.open(pdf_path)
    p = doc[page_idx]
    pix = p.get_pixmap(clip=rect, dpi=dpi)
    pix.save(out_path)
    print(f"Saved {out_path} ({pix.width}x{pix.height})")

# 1. Dantzig Portrait
crop_and_save("選修數學乙(下)課本_04_CH1_數學家小傳.pdf", 0, pymupdf.Rect(40, 40, 260, 260), "images/04_ch1_bio_dantzig.png")

# 2. Abel Portrait
crop_and_save("選修數學乙(下)課本_09_CH2_數學家小傳.pdf", 0, pymupdf.Rect(40, 40, 260, 260), "images/09_ch2_bio_abel.png")

# 3. CH2 學習活動 diagrams
# Page 1: complex plane with 6 roots
crop_and_save("選修數學乙(下)課本_07_CH2_學習活動.pdf", 0, pymupdf.Rect(200, 360, 420, 580), "images/07_ch2_act_fig1.png")
# Page 2: complex plane with 3 roots
crop_and_save("選修數學乙(下)課本_07_CH2_學習活動.pdf", 1, pymupdf.Rect(220, 240, 400, 440), "images/07_ch2_act_fig2.png")

# 4. CH2 綜合演練 (Problem 6 triangle diagram)
# Search for '如右圖' on page 2 (index 1)
doc_ch2_ex = pymupdf.open("選修數學乙(下)課本_08_CH2_綜合演練.pdf")
p = doc_ch2_ex[1]
# usually diagram is on the right side: x > 380
crop_and_save("選修數學乙(下)課本_08_CH2_綜合演練.pdf", 1, pymupdf.Rect(380, 160, 560, 340), "images/08_ch2_ex_p2_prob6.png")

# 5. CH3 學習活動 (Pinball machine)
# Page 1
crop_and_save("選修數學乙(下)課本_12_CH3_學習活動.pdf", 0, pymupdf.Rect(120, 380, 500, 680), "images/12_ch3_act_pinball.png")

# 6. CH1 學習活動 (Lotus farm table/graphic)
crop_and_save("選修數學乙(下)課本_03_CH1_學習活動.pdf", 0, pymupdf.Rect(60, 340, 550, 680), "images/03_ch1_act_p1_table.png")

# 7. 習題參考解答 (Linear programming graphs on page 1)
crop_and_save("選修數學乙(下)課本_17_習題參考解答.pdf", 0, pymupdf.Rect(340, 130, 550, 350), "images/15_sol_ex_ch1_fig1.png")
crop_and_save("選修數學乙(下)課本_17_習題參考解答.pdf", 0, pymupdf.Rect(340, 450, 550, 680), "images/15_sol_ex_ch1_fig2.png")
