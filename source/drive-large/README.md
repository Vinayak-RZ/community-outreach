# drive-large/ (on the box only)

Binary media for the 12 large Drive videos lives on the box at `/workspace/library/acads/community-outreach/source/drive-large/`, fetched from release [`raw-drive-videos-v1`](https://github.com/Vinayak-RZ/community-outreach/releases/tag/raw-drive-videos-v1).

This git folder holds only the inventory:

| File | What |
|---|---|
| `inventory.csv` | name, path, size_bytes, sha256, duration_s for every unzipped/rejoined file |
| `comparison.md` | pending vs received, duplicates vs `media/manifest.csv`, staging list |

Staged copies (hardlinks) for the pipeline worker: `/workspace/library/acads/community-outreach/media/staging-large/`.
