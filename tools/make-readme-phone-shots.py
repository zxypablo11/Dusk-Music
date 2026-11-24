"""Build framed phone README shots from fresh emulator captures (English UI)."""
from PIL import Image, ImageDraw, ImageFilter, ImageOps
from pathlib import Path

root = Path(__file__).resolve().parents[1]
src = {
    "home": root / "design/dusk/_emu/raw-home.png",
    "player": root / "design/dusk/_emu/raw-player.png",
    "settings": root / "design/dusk/_emu/raw-settings.png",
}
out_dir = root / "design/dusk"
shots = root / "site/shots"
shots.mkdir(parents=True, exist_ok=True)

W, H = 390, 844
RADIUS = 48
BEZEL = 10
PAD = 28


def phone_frame(img: Image.Image) -> Image.Image:
    img = ImageOps.fit(img.convert("RGBA"), (W, H), method=Image.Resampling.LANCZOS)
    mask = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(mask)
    d.rounded_rectangle((0, 0, W, H), RADIUS, fill=255)
    img.putalpha(mask)

    frame = Image.new("RGBA", (W + BEZEL * 2, H + BEZEL * 2), (0, 0, 0, 0))
    fmask = Image.new("L", frame.size, 0)
    fd = ImageDraw.Draw(fmask)
    fd.rounded_rectangle((0, 0, frame.size[0] - 1, frame.size[1] - 1), RADIUS + BEZEL, fill=255)
    bezel_img = Image.new("RGBA", frame.size, (18, 18, 20, 255))
    bezel_img.putalpha(fmask)
    frame.alpha_composite(bezel_img)
    frame.alpha_composite(img, (BEZEL, BEZEL))

    shadow = Image.new("RGBA", (frame.size[0] + 40, frame.size[1] + 40), (0, 0, 0, 0))
    sm = Image.new("L", shadow.size, 0)
    sd = ImageDraw.Draw(sm)
    sd.rounded_rectangle((20, 24, 20 + frame.size[0], 24 + frame.size[1]), RADIUS + BEZEL, fill=140)
    sh = Image.new("RGBA", shadow.size, (0, 0, 0, 255))
    sh.putalpha(sm)
    sh = sh.filter(ImageFilter.GaussianBlur(18))
    canvas = Image.new("RGBA", shadow.size, (0, 0, 0, 0))
    canvas.alpha_composite(sh)
    canvas.alpha_composite(frame, (20, 16))
    return canvas


phones = []
for key, path in src.items():
    if not path.exists():
        raise SystemExit(f"missing {path}")
    p = phone_frame(Image.open(path))
    phones.append(p)
    p.convert("RGB").save(out_dir / f"readme-ios-{key}.jpg", "JPEG", quality=92, optimize=True)
    p.convert("RGB").save(shots / f"ios-{key}.jpg", "JPEG", quality=90, optimize=True)
    p.save(shots / f"ios-{key}.webp", "WEBP", quality=88)

gap = 36
total_w = sum(p.size[0] for p in phones) + gap * (len(phones) - 1) + PAD * 2
total_h = max(p.size[1] for p in phones) + PAD * 2
bg = Image.new("RGB", (total_w, total_h), (12, 12, 14))
pix = bg.load()
for y in range(total_h):
    t = y / max(total_h - 1, 1)
    r = int(12 + 18 * t)
    g = int(12 + 10 * t)
    b = int(14 + 22 * t)
    for x in range(total_w):
        pix[x, y] = (r, g, b)

collage = bg.convert("RGBA")
x = PAD
max_h = max(p.size[1] for p in phones)
for p in phones:
    y = PAD + (max_h - p.size[1]) // 2
    collage.alpha_composite(p, (x, y))
    x += p.size[0] + gap

rgb = collage.convert("RGB")
rgb.save(out_dir / "readme-ios-trio.jpg", "JPEG", quality=93, optimize=True)
rgb.save(out_dir / "app-integrated.jpg", "JPEG", quality=93, optimize=True)
print("wrote English phone previews", rgb.size)
