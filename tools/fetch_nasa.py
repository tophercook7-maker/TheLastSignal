#!/usr/bin/env python3
"""Fetch curated NASA public-domain space imagery for Answering the Dark.
Uses the free images-api.nasa.gov (no key). Saves optimized JPGs to live/assets/img/.
"""
import json, os, urllib.request, io
from PIL import Image

OUT = os.path.join(os.path.dirname(__file__), "..", "live", "assets", "img")
os.makedirs(OUT, exist_ok=True)

# filename -> search query (NASA public domain)
WANT = {
    "deepfield":   "webb first deep field",
    "carina":      "cosmic cliffs carina nebula",
    "pillars":     "pillars of creation webb",
    "neptune":     "neptune voyager 2",
    "sun":         "solar flare sun",
    "aurora":      "aurora from international space station",
    "galaxy":      "spiral galaxy hubble",
    "cluster":     "globular star cluster hubble",
    "nebula_blue": "veil nebula",
    "carina_wide": "carina nebula panorama",
    "earthnight":  "earth at night from space",
    "field_stars": "hubble ultra deep field",
}

def get(url, timeout=40):
    req = urllib.request.Request(url, headers={"User-Agent": "atd-fetch"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()

def search_image(query):
    api = "https://images-api.nasa.gov/search?media_type=image&q=" + urllib.parse.quote(query)
    data = json.loads(get(api))
    for item in data["collection"]["items"]:
        href = item.get("href")
        if not href:
            continue
        try:
            files = json.loads(get(href))
        except Exception:
            continue
        # prefer ~large, else ~medium, else the biggest non-thumb jpg
        pick = None
        for suffix in ("~large.jpg", "~medium.jpg", "~orig.jpg"):
            for f in files:
                if f.lower().endswith(suffix):
                    pick = f; break
            if pick: break
        if not pick:
            jpgs = [f for f in files if f.lower().endswith(".jpg") and "thumb" not in f.lower()]
            pick = jpgs[0] if jpgs else None
        if pick:
            return pick.replace("http://", "https://")
    return None

import urllib.parse
def main():
    for name, query in WANT.items():
        dest = os.path.join(OUT, name + ".jpg")
        if os.path.exists(dest):
            print("skip", name); continue
        try:
            url = search_image(query)
            if not url:
                print("NO RESULT", name); continue
            img = Image.open(io.BytesIO(get(url))).convert("RGB")
            # cover-crop-ish: cap long side at 1600
            img.thumbnail((1600, 1600))
            img.save(dest, "JPEG", quality=82, optimize=True)
            print(f"ok {name}: {img.size} <- {url.split('/')[-1]}")
        except Exception as e:
            print(f"FAIL {name}: {e}")

if __name__ == "__main__":
    main()
