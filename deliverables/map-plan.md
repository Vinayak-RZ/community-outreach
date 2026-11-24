# Campus map plan

## Base map: what we used
We looked for an official IIT Roorkee campus map first. iitr.ac.in has campus pages but we found no clean map image or PDF on it. The only full list we found was a numbered map PDF on a third-party notes site, which we can't credit or trace from. So the base is **OpenStreetMap**: `analysis/data/osm/iitr-campus-2026-10-20.osm` (OSM API extract, 20 Oct 2026), parsed by `analysis/scripts/osm_parse.py`. Licence: ODbL 1.0. Credit on every map: "Map data © OpenStreetMap contributors".

- `analysis/figures/fig12_campus_basemap.png` / `.svg`: base map
- `analysis/figures/fig13_hotspot_map_draft.png` / `.svg`: hotspot draft
- `analysis/data/places.csv`: one row per place mention (keyword match, `match` = exact or uncertain)
- `analysis/data/places-summary.csv`: counts per place
- `analysis/data/places-osm-match.csv`: map position and where it came from

## How the counts work
- The circles count mentions in the interview transcripts, the survey free text, the CCF meet and the CMO notes. The WhatsApp chat is left out of the circles because it's mostly us planning ("meet at ICC", "go to the hospital"), not people describing dogs.
- The CCF meet transcript is the same recording as "Recording 2026-09-25 163540", so we only count it once. Treat the counts as rough.
- Team-confirmed hotspots (our own fieldwork, 20 Oct): outside Himalaya Bhawan, outside MAC, around the Architecture dept, between Govind Bhawan and Chemistry, near Jawahar Bhawan. These show as rings and aren't added to the counts.
- "KB" and "JB" in the chat are usually Hindi (kab, jab), so they don't count there. In transcripts they count but are marked uncertain.

## What the map can show
| Layer | Support | Notes |
|---|---|---|
| Hotspots by issue | OK for Himalaya, Govind–Chemistry, Kasturba, Hospital, SAC, Rajiv | Most places have under 10 mentions |
| Team-confirmed hotspots | Good for 4 of 5 | MAC isn't in OSM, so it isn't placed yet |
| Interview spots | OK | Taken from file names (guard, canteen, Neh Road, Archi dept) |
| Night notes | Thin | 21 night/late mentions in total, a few per place |
| Places named in the survey | Thin | Few survey answers name a place |
| Chase routes | Very thin | Only one or two described a route (e.g. "around KB's route"). Better left for the hotspot walk |
| Feeding zones vs where dogs gather | Not possible yet | The chats and CCF talk about "feeding spots", a feeder going once or twice a day, and a feeding team, but never name a spot |
| Boundary gaps | Not placed | 11 boundary mentions plus gate 7 and gate 5, with no position |

## Positions added from Vinayak (20 Oct)
- MAC: between Radhakrishnan and Rajiv (approx.).
- MNC: in front of Himalaya, towards Govind and ICC (approx.).
- Feeding spots: one near Mechanical, one near Kasturba. Positions are approx. and labelled that way.
- Mandir is Saraswati Mandir. The Govind–Chemistry spot is right.
- Gate 7 and the wall gaps are still not placed.

## Places missing from OSM
MAC, MNC, gate 7, gate 5, the boundary gaps, the badminton hall, the Robocon lab, Vivekananda Bhawan, plus which mess or canteen people mean. Rajiv, Radhakrishnan and Himalaya are there as OSM entries but not as building outlines we parsed, so they use the Nominatim position.

## Layout options for the poster centre
1. **Map in the middle.** Full-width map with circles and rings, a 2–3 line key, and night counts as small notes next to each place. The findings sit around it.
2. **Map plus side list.** Map on the left two thirds, and on the right a short ranked list (place, mentions, main issue) that also covers MAC and MNC, which can't be placed.
3. **Map with callouts.** Five team hotspots numbered on the map, each with a one-line callout (what happens there, day or night).

The poster uses option 2: the map on the left, the key and "Who brought up what" bars on the right.

## Later walk map (deck)

A separate team-walk map is used on slide 3 of the deck. Source note: [`evidence/hotspot-walk-map.md`](../evidence/hotspot-walk-map.md). Image: `deliverables/posters/assets/hotspot-walk-map.jpg`. It ranks dogs seen on a walk (counts not kept) and plots feeding spots as told by CCF or feeders. It is not the mention map in fig13, and it does not meet the KPI Record row.
