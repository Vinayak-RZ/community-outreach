# Transcript spot-checks

Three transcripts were checked on 20/10/2026 by running a second, independent pass with a different model
(faster-whisper `small`, float32, CPU, same language setting, no silence filter) and comparing it word by word
with the `medium` transcript in this folder. Agreement is the share of `medium` words that the `small` pass
also produced, in order. Confidence is Whisper's own per-word probability from the `medium` pass.

Neither model is ground truth. Where they disagree, or where confidence is low, a person should listen to the
audio before quoting it. The raw numbers and the second-pass text are kept on the box in
`media/logs/spotcheck/` and are not committed.

| Transcript | Language | Length | Agreement | Mean word confidence | Words below 0.5 |
|---|---|---|---|---|---|
| Cautley Bhawan | English (auto-detected) | 5:00 | 82% | 0.75 | 20% |
| Agrim | Hindi with English words | 2:53 | 46% | 0.77 | 7% |
| Malishka pt1 | English (forced re-run) | 2:57 | 92% | 0.85 | 11% |

## What this says

- The English transcripts are reliable for the gist. Most disagreements are filler words, and the two models
  agree on the substance.
- The Hindi transcript needs the most human checking. The `small` model is weak at Hindi and writes English words
  in Devanagari, so 46% understates the real accuracy, but it also means the second pass can't vouch for the
  Hindi lines. Treat Hindi transcripts as a guide to where things are said, not as quotable text.
- Numbers, hostel names and medical details are where the models slip most, and those are exactly the parts a
  report is likely to quote.

## Timestamps to listen to

### Cautley Bhawan (English)

- **0:08-0:12**: the hostel names where dogs are calmer. The transcript reads "Himalaya, Pasirba or Sairoshni",
  which look like mis-hearings of bhawan names. Check before citing.
- **0:57-1:07**: the number of vaccine doses ("6-9 doses"; the second pass heard "69"). Verify the number.
- **1:17-1:22**: "it is short" versus "it's a shot" in the answer about the medical procedure.
- **1:42-1:56**: walking around at night and whether dogs "invade" the lab; the two passes word this differently.
- **1:56-2:13**: the hygiene question about hostels and canteens; low confidence and the passes disagree.
- **2:55-3:20**: the lowest-confidence stretch of the file (mean log probability -0.58), including the remark
  about designated caretakers at one hostel.
- **3:57-4:40**: the closing recommendations to the campus authority. Agreement drops to about 70% here, and the
  second pass is missing or rewords several lines ("it is going to be too much of an issue", the answer at 4:38).

### Agrim (Hindi)

- **0:00-0:26**: the introduction and the speaker's department and year; the two passes barely overlap.
- **1:12-1:32**: the lowest-confidence stretch (mean log probability -0.64): the story of a dog sleeping next to a
  friend in his room.
- **1:42-1:53**: the CMO's advice that even a scratch counts as a bite, and the rabies concern. This is a likely
  quote and the second pass disagrees heavily.
- **1:56-2:11**: dogs around MAC, MNC and SAC and whether that is acceptable.
- **2:34-2:50**: the designated shelters suggestion. The second pass has extra speech here that the `medium`
  transcript lacks, so some words may be missing.

### Malishka pt1 (English)

- **0:07-0:14**: the speaker's year and branch (low confidence on the opening words).
- **1:39-1:50**: having to see a doctor before the vaccine at night; the word "doctor" has very low confidence
  (0.01), though both passes agree on the meaning.
- **1:58-2:14**: the vaccine schedule (48 hours, five doses over two months). Both passes agree, but it's a
  medical detail, so confirm before quoting.
- **2:25-2:35**: the recording breaks off; the passes disagree, and this part has no interview content.
