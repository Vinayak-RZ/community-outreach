"""Parse the OSM extract (© OpenStreetMap contributors, ODbL 1.0) into simple JSON layers."""
import xml.etree.ElementTree as ET, json, sys
src = sys.argv[1] if len(sys.argv) > 1 else "analysis/data/osm/iitr-campus-2026-10-20.osm"
r = ET.parse(src).getroot()
nodes = {n.get("id"): (float(n.get("lon")), float(n.get("lat"))) for n in r.iter("node")}
out = {"buildings": [], "roads": [], "green": [], "water": [], "boundary": [], "named": []}
for w in r.iter("way"):
    t = {k.get("k"): k.get("v") for k in w.iter("tag")}
    pts = [nodes[n.get("ref")] for n in w.iter("nd") if n.get("ref") in nodes]
    if len(pts) < 2: continue
    f = {"name": t.get("name", ""), "pts": pts, "tags": t}
    if "building" in t: out["buildings"].append(f)
    elif "highway" in t and t["highway"] not in ("footway", "path", "steps", "corridor"): out["roads"].append(f)
    elif t.get("leisure") in ("park", "pitch", "garden", "stadium", "sports_centre") or t.get("landuse") in ("grass", "recreation_ground"): out["green"].append(f)
    elif t.get("natural") == "water" or "waterway" in t: out["water"].append(f)
    if t.get("amenity") == "university" or (t.get("barrier") == "wall"): out["boundary"].append(f)
    if t.get("name"):
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        out["named"].append({"name": t["name"], "lon": sum(xs)/len(xs), "lat": sum(ys)/len(ys), "kind": t.get("building") or t.get("highway") or t.get("amenity") or ""})
for n in r.iter("node"):
    t = {k.get("k"): k.get("v") for k in n.iter("tag")}
    if t.get("name"): out["named"].append({"name": t["name"], "lon": float(n.get("lon")), "lat": float(n.get("lat")), "kind": t.get("amenity", "node")})
for m in r.iter("relation"):
    t = {k.get("k"): k.get("v") for k in m.iter("tag")}
    if t.get("amenity") == "university": print("relation university", t.get("name"))
json.dump(out, open("analysis/data/osm/layers.json", "w"))
print({k: len(v) for k, v in out.items()})
