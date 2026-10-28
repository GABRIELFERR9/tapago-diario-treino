# -*- coding: utf-8 -*-
"""Gera icon.png (1024) e splash.png (2732) do Tá Pago — carimbo sobre papel."""
from PIL import Image, ImageDraw, ImageFont

PAPEL = (239, 236, 228)
TINTA = (194, 36, 47)


def carimbo(texto, fs, pad_x, pad_y, borda, gap):
    """Desenha o carimbo (borda dupla + texto) e devolve a imagem rotacionada."""
    font = ImageFont.truetype(r"C:\Windows\Fonts\ariblk.ttf", fs)
    tmp = Image.new("RGBA", (10, 10))
    d = ImageDraw.Draw(tmp)
    box = d.textbbox((0, 0), texto, font=font)
    tw, th = box[2] - box[0], box[3] - box[1]
    w, h = tw + pad_x * 2, th + pad_y * 2
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, w - 1, h - 1], outline=TINTA, width=borda)
    off = borda + gap
    d.rectangle([off, off, w - 1 - off, h - 1 - off], outline=TINTA, width=borda)
    d.text((pad_x - box[0], pad_y - box[1]), texto, font=font, fill=TINTA)
    return img.rotate(8, expand=True, resample=Image.BICUBIC)


# ── ícone 1024x1024 ──
icone = Image.new("RGBA", (1024, 1024), PAPEL)
st = carimbo("TÁ\nPAGO", 210, 70, 46, 16, 14)
# fonte multiline não centraliza sozinha; refaz com draw.multiline
def carimbo_multi(linhas, fs, pad, borda, gap):
    font = ImageFont.truetype(r"C:\Windows\Fonts\ariblk.ttf", fs)
    tmp = Image.new("RGBA", (10, 10)); d = ImageDraw.Draw(tmp)
    box = d.multiline_textbbox((0, 0), linhas, font=font, spacing=18, align="center")
    tw, th = int(box[2] - box[0]), int(box[3] - box[1])
    w, h = int(tw + pad * 2), int(th + pad * 2)
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    d.rectangle([0, 0, w - 1, h - 1], outline=TINTA, width=borda)
    off = borda + gap
    d.rectangle([off, off, w - 1 - off, h - 1 - off], outline=TINTA, width=borda)
    d.multiline_text((pad - box[0], pad - box[1]), linhas, font=font, fill=TINTA, spacing=18, align="center")
    return img.rotate(8, expand=True, resample=Image.BICUBIC)

st = carimbo_multi("TÁ\nPAGO", 235, 78, 18, 15)
st.thumbnail((880, 880), Image.LANCZOS)
icone.alpha_composite(st, ((1024 - st.width) // 2, (1024 - st.height) // 2))
icone.convert("RGB").save("assets/icon.png")

# ── splash 2732x2732 ──
splash = Image.new("RGBA", (2732, 2732), PAPEL)
st2 = carimbo_multi("TÁ PAGO", 300, 110, 22, 20)
splash.alpha_composite(st2, ((2732 - st2.width) // 2, (2732 - st2.height) // 2 - 60))
# linha de rodapé
f2 = ImageFont.truetype(r"C:\Windows\Fonts\cour.ttf", 64)
d = ImageDraw.Draw(splash)
txt = "COMPROVANTE DIÁRIO DE TREINO"
box = d.textbbox((0, 0), txt, font=f2)
d.text(((2732 - (box[2] - box[0])) // 2, (2732 + st2.height) // 2 + 40), txt, font=f2, fill=(76, 78, 82))
splash.convert("RGB").save("assets/splash.png")
print("icon.png e splash.png gerados")
