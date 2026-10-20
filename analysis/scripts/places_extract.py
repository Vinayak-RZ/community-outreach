"""Build analysis/data/places.csv: every place mention in transcripts (English passes), survey free text,
the team WhatsApp chat, the CCF GMeet transcript and the CMO notes. Keyword-based, so each row is a
machine match: 'match' says exact or uncertain (fuzzy spelling / machine-transcript mishearing)."""
import re, csv, pathlib, collections
R = pathlib.Path(__file__).resolve().parents[2]
PLACES = [  # (normalised name, exact regex, uncertain regex)
 ("Himalaya Bhawan", r"himalaya", r"himalayas|himaliya|himalya"),
 ("MAC", r"\bmac\b", r"\bmack\b"),
 ("SAC", r"\bsac\b", r"\bsack\b"),
 ("Mandir", r"mandir|temple", r""),
 ("Library", r"librar", r""),
 ("Gate 7", r"gate (no\.? ?|number )?7|gate seven", r""),
 ("Gate 5", r"gate (no\.? ?|number )?5", r""),
 ("Gate 6", r"gate (no\.? ?|number )?6", r""),
 ("Main gate", r"main gate", r""),
 ("Boundary wall/railing", r"boundary|railing|\bwall\b", r""),
 ("Nehru Road", r"nehru road|neh road", r""),
 ("MNC", r"\bmnc\b|\bm ?& ?c\b", r"\bmnc\w*"),
 ("Govind Bhawan", r"govind", r""),
 ("Rajiv Bhawan", r"rajiv|\brjb\b", r""),
 ("Rajendra Bhawan", r"rajendra", r""),
 ("Jawahar Bhawan", r"jawahar", r"\bjb\b"),
 ("Sarojini Bhawan", r"sarojini|sarojni", r"saroshni|sairoshni"),
 ("Kasturba Bhawan", r"kasturba", r"\bkb\b|kasurva|pasirba"),
 ("Cautley Bhawan", r"cautley", r""),
 ("Radhakrishnan Bhawan", r"radhakrishnan|\brkb\b", r""),
 ("Vivekananda Bhawan", r"vivekanand", r""),
 ("Azad Bhawan", r"\bazad\b", r""),
 ("Ravindra Bhawan", r"ravindra", r""),
 ("Architecture dept", r"archi(tecture)?\b|archi dept", r""),
 ("Physics / Chemistry dept", r"physics|\bchem(istry)? (dept|department)|\bchem\b|\bphy\b", r""),
 ("LBS ground", r"\blbs\b", r""),
 ("LHC", r"\blhc\b", r""),
 ("ICC", r"\bicc\b", r""),
 ("Badminton hall", r"badminton", r""),
 ("Thomson lane/road", r"thomson|thomaso", r"thomswalla"),
 ("Aravali", r"aravali", r""),
 ("Hospital", r"hospital|health cent", r""),
 ("Mess / canteen", r"\bmess\b|canteen|cafe", r""),
 ("Feeding zone (unnamed)", r"feeding (zone|spot|point|area)s?", r""),
 ("Robocon lab", r"robocon", r"robocoin"),
 ("Saraswati Mandir", r"saraswati", r""),
]
TYPES = [("bite", r"\bbit(e|ten|es)\b|rabies|vaccin|scratch"), ("chasing", r"chas|ran at|run after|attack|follow"),
 ("dogs in hostel", r"room|hostel|bhawan.*(enter|inside)|inside the|washroom|floor"), ("feeding zone", r"feed"),
 ("boundary gap", r"boundary|broken|gap|railing|wall|outside dogs|from outside"), ("puppies", r"pupp|pups|litter|children grow"),
 ("noise", r"bark|noise|howl"), ("garbage", r"garbage|dustbin|bin\b|waste|trash"), ("shelter or care", r"shelter|medical|care|injur|vet"),
 ("positive", r"friendly|calm|love|cute|fine with|harmony")]
NIGHT = r"night|2 ?am|late|dark|evening|12\.?30"
INTERVIEWED = {"Jawahar Bhawan": "Jawahar bhawan guard; Jawahar rishit", "Sarojini Bhawan": "Sarojini bhawan guard; Sarojni Canteen", "Cautley Bhawan": "Cautley Bhawan; Cautley Bhawan 2",
 "MAC": "Mac guard; Mac balu; IMG_9408 (Robocon lab, MAC 4th floor)", "MNC": "Mnc guard", "Nehru Road": "Neh Road 2-4", "Architecture dept": "Archi dept ma'am",
 "Mess / canteen": "Sarojni Canteen; VK canteen bhaiya", "Hospital": "13/10 hospital-day clips; CMO (notes)", "Himalaya Bhawan": "IMG_5268 (caretaker, Himalaya side; inferred)", "Robocon lab": "ROBOCON; IMG_9408"}
def classify(t):
    ty = [n for n, rx in TYPES if re.search(rx, t, re.I)]
    return ";".join(ty) or "mention only"
rows = []
def scan(src, ref, text, ctx):
    for name, ex, un in PLACES:
        m = re.search(ex, text, re.I); match = "exact"
        if not m and un and not src.startswith("WhatsApp"): m = re.search(un, text, re.I); match = "uncertain"  # KB/JB are Hinglish words (kab/jab) in chat
        if m:
            rows.append(dict(place=name, source=src, where=ref, mention_type=classify(ctx), time_of_day="night/late" if re.search(NIGHT, ctx, re.I) else "",
                             interviewed_here="yes" if name in INTERVIEWED else "", match=match, text=text.strip()[:160]))
for f in sorted((R/"transcripts").glob("*/*.en.txt")):
    L = f.read_text(encoding="utf-8").splitlines()
    for i, l in enumerate(L):
        m = re.match(r"\[(\d\d:\d\d:\d\d)\]\s*(.*)", l)
        if not m: continue
        ctx = " ".join(x.split("]",1)[-1] for x in L[max(0,i-1):i+2])
        scan("transcripts/"+f.parent.name, m.group(1), m.group(2), ctx)
for r in csv.DictReader(open(R/"source/survey/survey-responses.csv", encoding="utf-8")):
    t = r["What would a fair solution look like for both students and dogs?"] or ""
    if t: scan("survey free text", "row "+r["sheet_row"], t, t)
for i, l in enumerate(open(R/"source/whatsapp/raw-transcript.txt", encoding="utf-8")):
    if l.startswith("[") : scan("WhatsApp comm outreach", "line %d" % (i+1), l.split(": ",1)[-1], l)
for i, l in enumerate(open(R/"source/ccf-gmeet-transcript.txt", encoding="utf-8")):
    scan("CCF GMeet transcript", "line %d" % (i+1), l, l)
for i, l in enumerate(open(R/"project-brief.md", encoding="utf-8")):
    if "CMO (13/10" in l or "Gate 5 guards (14/10)" in l: scan("CMO / gate-5 notes (project-brief.md)", "line %d" % (i+1), l, l)
LOC = [("Jawahar Bhawan","Jawahar bhawan guard"),("Jawahar Bhawan","Jawahar rishit"),("Sarojini Bhawan","Sarojini bhawan guard"),("Mess / canteen","Sarojni Canteen"),("Mess / canteen","VK canteen bhaiya"),
 ("Cautley Bhawan","Cautley Bhawan"),("Cautley Bhawan","Cautley Bhawan 2"),("MAC","Mac guard"),("MAC","Mac balu"),("MAC","IMG_9408"),("Robocon lab","ROBOCON"),("MNC","Mnc guard"),
 ("Nehru Road","Neh Road 2"),("Nehru Road","Neh Road 3"),("Nehru Road","Neh Road 4"),("Architecture dept","Archi dept ma\u2019am"),("Hospital","20261013_120605"),("Hospital","20261013_120723"),("Himalaya Bhawan","IMG_5268")]
for place, fn in LOC:
    rows.append(dict(place=place, source="transcripts/"+fn, where="file (interview location from file name or transcript)", mention_type="interview location", time_of_day="",
                     interviewed_here="yes", match="uncertain" if fn in ("IMG_5268","Mac balu") else "exact", text=""))
# Team field observations confirmed by Vinayak on 20 Oct 2026 (hotspots, not counted as interview mentions)
for place in ["Himalaya Bhawan","MAC","Architecture dept","Govind Bhawan (towards Chemistry)","Jawahar Bhawan"]:
    rows.append(dict(place=place, source="team field observation", where="20 Oct 2026", mention_type="hotspot (team)", time_of_day="",
                     interviewed_here="", match="exact", text="Confirmed hotspot from our own fieldwork"))
# drop noise: the CCF GMeet is the same meeting as transcripts/Recording 2026-09-25 163540 (kept both, flagged)
with open(R/"analysis/data/places.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
cnt = collections.Counter(r["place"] for r in rows); srcs = collections.defaultdict(set)
for r in rows: srcs[r["place"]].add(r["source"])
with open(R/"analysis/data/places-summary.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["place", "mentions", "distinct_sources", "uncertain_mentions", "night_mentions", "interviewed_here", "top_types"])
    for p, n in cnt.most_common():
        sub = [r for r in rows if r["place"] == p]
        ty = collections.Counter(t for r in sub for t in r["mention_type"].split(";") if t != "mention only")
        w.writerow([p, n, len(srcs[p]), sum(r["match"] == "uncertain" for r in sub), sum(bool(r["time_of_day"]) for r in sub), INTERVIEWED.get(p, ""), "; ".join(f"{k} {v}" for k, v in ty.most_common(3))])
print(len(rows)); [print(p, n, len(srcs[p])) for p, n in cnt.most_common(40)]
