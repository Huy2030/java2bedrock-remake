import json, glob, re, os

def nn(v):
    if not v or ':' not in v or v.startswith('#'):
        return v
    i = v.index(':')
    ns = v[:i]
    rest = v[i+1:]
    tex_path = f"./assets/{ns}/textures/{rest}.png"
    if os.path.exists(tex_path):
        return v
    cleaned = re.sub(r'^(_b_|_)', '', ns)
    return f"{cleaned}:{rest}"

for f in glob.glob("./assets/**/*.json", recursive=True):
    try:
        d = json.load(open(f, encoding="utf-8"))
        tx = d.get("textures")
        if not isinstance(tx, dict):
            continue
        c = False
        for k, v in tx.items():
            nv = nn(v)
            if nv != v:
                tx[k] = nv
                c = True
        if c:
            json.dump(d, open(f, "w", encoding="utf-8"), separators=(',', ':'), ensure_ascii=False)
    except:
        pass
