from PIL import Image
from io import BytesIO
import glob, os, json, math

lines = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, "a", "b", "c", "d", "e", "f"]

try:
    with open("pack/assets/minecraft/font/default.json", "r") as f:
        data = json.load(f)
except Exception as e:
    exit(1)

symbols = []
paths = []
heights = []
ascents = []
for d in data['providers']:
    try:
        symbols.append(d['chars'])
        paths.append(d['file'])
        heights.append(d['height'])
        ascents.append(d['ascent'])
    except:
        continue

def createfolder(glyph):
    os.makedirs(f"images/{glyph}", exist_ok=True)
    os.makedirs(f"export/{glyph}", exist_ok=True)
    os.makedirs(f"font/", exist_ok=True)

def create_empty(glyph, blankimg):
    for line in lines:
        for linee in lines:
            if linee != lines:
                name = f"{line}{linee}"
                if not os.path.isfile(f"images/{glyph}/0x{glyph}{name}.png"):
                    imagesus = Image.open(blankimg)
                    image = imagesus.copy()
                    image.save(f"images/{glyph}/0x{glyph}{name}.png", "PNG")
    for line in lines:
        name = f"{line}{line}"
        if not os.path.isfile(f"images/{glyph}/0x{glyph}{name}.png"):
            imagesus = Image.open(blankimg)
            image = imagesus.copy()
            image.save(f"images/{glyph}/0x{glyph}{name}.png", "PNG")

def imagetoexport(glyph, blankimg):
    filelist = [file for file in os.listdir(f'images/{glyph}') if file.endswith('.png')]
    for img in filelist:
        image = Image.open(blankimg)
        logo = Image.open(f'images/{glyph}/{img}')
        image_copy = image.copy()
        w, h = image.size
        wl, hl = logo.size
        for height, symboll in zip(heights, symbols):
            symbolbe = ''.join(symboll)
            symbolbehex = hex(ord(symbolbe))
            if len(symbolbehex) == 6:
                symbol = symbolbehex[4:]
            elif len(symbolbehex) == 5:
                symbolbehex = symbolbehex[:2] + "0" + symbolbehex[2:]
                symbol = symbolbehex[4:]
            name = f"0x{glyph}{symbol}"
            imgname = f"0x{glyph}{img}"
            if name == imgname:
                if height >= 1 and height < w and height < h:
                    size = (height, height)
                    logo.thumbnail(size, Image.ANTIALIAS)
                if wl > (w / 2) and hl > (h / 2):
                    position = (0, 0)
                    image_copy.paste(logo, position)
                    image_copy.save(f"export/{glyph}/{img}")
                else:
                    position = (0, (h // 2) - (hl // 2))
                    image_copy.paste(logo, position)
                    image_copy.save(f"export/{glyph}/{img}")

def sprite(glyph, spritesheet=None, tile=None):
    max_frames_row = 16.0
    frames = []
    if tile is None:
        tile_width = tile_height = 256
        spritesheet_width = spritesheet_height = 4096
    else:
        tile_width = tile_height = tile
        spritesheet_width = spritesheet_height = spritesheet
    files = sorted(os.listdir(f"export/{glyph}"))
    for current_file in files:
        try:
            with Image.open(f"export/{glyph}/{current_file}") as im:
                frames.append(im.getdata())
        except:
            pass
    tile_width = frames[0].size[0]
    tile_height = frames[0].size[1]
    if len(frames) > max_frames_row:
        spritesheet_width = tile_width * max_frames_row
        required_rows = math.ceil(len(frames) / max_frames_row)
        spritesheet_height = tile_height * required_rows
    else:
        spritesheet_width = tile_width * len(frames)
        spritesheet_height = tile_height
    spritesheet_img = Image.new("RGBA", (int(spritesheet_width), int(spritesheet_height)))
    for current_frame in frames:
        top = tile_height * math.floor(frames.index(current_frame) / max_frames_row)
        left = tile_width * (frames.index(current_frame) % max_frames_row)
        bottom = top + tile_height
        right = left + tile_width
        box = [int(i) for i in (left, top, right, bottom)]
        cut_frame = current_frame.crop((0, 0, tile_width, tile_height))
        spritesheet_img.paste(cut_frame, box)
    os.makedirs("staging/target/rp/font", exist_ok=True)
    spritesheet_img.save(f"staging/target/rp/font/glyph_{glyph}.png", "PNG")

glyphs = []
for i in symbols:
    if i not in glyphs:
        try:
            symbolbe = ''.join(i)
            sbh = hex(ord(symbolbe))
            a = sbh[2:]
            ab = a[:2]
            glyphs.append(ab.upper())
        except:
            symbols.remove(i)
            continue

glyphs = list(dict.fromkeys(glyphs))

listglyphdone = []

def converterpack(glyph):
    createfolder(glyph)
    if len(symbols) != len(paths):
        return
    maxsw, maxsh = 0, 0
    for symboll, path in zip(symbols, paths):
        symbolbe = ''.join(symboll)
        symbolbehex = hex(ord(symbolbe))
        if glyph in listglyphdone:
            return False
        if len(symbolbehex) == 6:
            symbol = symbolbehex[4:]
            symbolac = symbolbehex[2:]
            symbolcheck = symbolac[:2]
        elif len(symbolbehex) == 5:
            symbolbehex = symbolbehex[:2] + "0" + symbolbehex[2:]
            symbol = symbolbehex[4:]
            symbolac = symbolbehex[2:]
            symbolcheck = symbolac[:2]
        glyphs.append(symbolcheck.upper())
        if symbolcheck.upper() == glyph.upper():
            if ":" in path:
                try:
                    namespace = path.split(":")[0]
                    pathnew = path.split(":")[1]
                    imagefont = Image.open(f"pack/assets/{namespace}/textures/{pathnew}")
                    image = imagefont.copy()
                    image.save(f"images/{glyph}/0x{glyph}{symbol}.png", "PNG")
                except Exception as e:
                    print(e)
                    continue
            else:
                try:
                    imagefont = Image.open(f"pack/assets/minecraft/textures/{path}")
                    image = imagefont.copy()
                    image.save(f"images/{glyph}/0x{glyph}{symbol}.png", "PNG")
                except Exception as e:
                    print(e)
                    continue
        else:
            continue
    files = glob.glob(f"images/{glyph}/*.png")
    for file in files:
        image = Image.open(file)
        sw, sh = image.size
        maxsw, maxsh = max(maxsw, sw), max(maxsh, sh)
    maxdim = max(maxsw, maxsh)
    size = (int(maxdim + 1), int(maxdim + 1))
    if size == (0, 0):
        return
    glyphsize = size[0] * 16
    img = Image.open("empty.png")
    imgre = img.resize(size)
    imgre.save("blankimg.png")
    blankimg = "blankimg.png"
    create_empty(glyph, blankimg)
    imagetoexport(glyph, blankimg)
    sprite(glyph, glyphsize, size[0])
    listglyphdone.append(glyph)

for glyph in glyphs:
    converterpack(glyph)
