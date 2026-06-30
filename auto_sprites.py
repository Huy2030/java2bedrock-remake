import json, os

def build_texture_path(e):
    ns, mp, mn = e.get("namespace",""), e.get("model_path",""), e.get("model_name","")
    if not ns or not mn: return None
    return f"textures/{ns}/{mp}/{mn}" if mp else f"textures/{ns}/{mn}"

def main():
    config_path = "staging/config.json"
    if not os.path.exists(config_path): return 1
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    texture_data = {}
    for gid, entry in config.items():
        if not isinstance(entry, dict): continue
        path_hash = entry.get("path_hash", "")
        tex_path = build_texture_path(entry)
        if path_hash and tex_path and path_hash not in texture_data:
            texture_data[path_hash] = {"textures": tex_path}
    item_texture_path = "staging/target/rp/textures/item_texture.json"
    os.makedirs(os.path.dirname(item_texture_path), exist_ok=True)
    with open(item_texture_path, "w", encoding="utf-8") as f:
        json.dump({"texture_data": texture_data}, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
