import pymupdf
import re
import os

doc = pymupdf.open("選修數學乙(下)課本_05_CH2-1_複數.pdf")
p = doc[2] # page 3
# Cardano is at x: 420-530, y: 150-320
rect = pymupdf.Rect(430, 150, 520, 315)
pix = p.get_pixmap(clip=rect, dpi=200)
pix.save("images/05_ch2_1_p3_圖1_卡丹.png")
print("Saved Cardano:", pix.width, "x", pix.height)
