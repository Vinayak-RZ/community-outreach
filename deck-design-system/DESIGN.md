# Deck design system

Fixed-format **1920 × 1080** HTML decks. Light canvas, coral accent, near-black cover. One idea per slide. Typography and space carry hierarchy — not cards everywhere.

This file is the contract. Example HTMLs show how to apply it. Do not invent a second visual language.

---

## Frame

| Token | Value | Role |
|---|---|---|
| Slide | `1920 × 1080` | Always. Scale with `--s` for on-screen fit. |
| Side margin | `128px` | `.hd` / `.ct` / `.foot` left & right |
| Header top | `96px` | `.hd` |
| Content top | `388px` default | `.ct` — raise (`top: 248–330px`) when the header is short |
| Content bottom | `136px` | Keep-out above footer |
| Footer | `40px` from bottom | Brand left · optional source centre · page right |

Content never spills the slide. Decoration may bleed; type and panels may not.

---

## Colour (by role)

| Role | Token | Hex |
|---|---|---|
| Canvas | `--canvas` | `#FAFAF9` |
| Surface / card | `--surface` | `#FFFFFF` |
| Quiet band | `--band` | `#F1F1EF` |
| Border | `--border` / `--border-strong` | `#E2E2DF` / `#CFCFCB` |
| Primary ink | `--ink` | `#191c1a` |
| Secondary ink | `--ink2` | `#4B4D4A` |
| Muted / labels | `--muted` | `#6E706C` |
| Accent | `--accent` | `#F75440` |
| Accent deep | `--accent-deep` | `#C2361F` |
| Accent wash | `--accent-soft` / `--accent-wash` | `#FFF3F0` / `#FFE3DC` |
| Cover field | `--cover` | `#000a07` |

**Rules**

- One accent. Use it for the point: key number, active column, highlight border, page rule.
- Do not tint every heading coral.
- Cover slides are dark (`--cover`). Everything else defaults light.
- Flat finish: no drop shadows except the light product-stack elevation already in `.band-item`. No glow, no purple gradients.

To rebrand: override the tokens in `:root`. Keep the role names.

---

## Type

| Role | Face | Typical sizes |
|---|---|---|
| Display / headlines | Space Grotesk 500–600 | Cover word ~200px · `.h` 88px · section titles 32–44px · big stats 96–136px |
| Body | Geist 400 | Sub 32px · body copy 24–28px |
| Labels / page / keys | Geist Mono | 20–24px, uppercase, letter-spacing ~0.06–0.14em |

**Rules**

- Hierarchy by size + weight + colour, not by bolding everything.
- Big numbers use `font-variant-numeric: tabular-nums` (`.num`).
- Headlines: negative letter-spacing (`-0.02em` to `-0.05em`).
- No synthetic italics. No Inter / Roboto / system UI as the brand face.

Fonts live in `fonts/` and load via `css/fonts.css`.

---

## Chrome

Every content slide (not the cover) uses:

```html
<section class="slide">
  <div class="hd">
    <h1 class="h">One clear headline</h1>
    <p class="sub">Optional supporting line.</p>
  </div>
  <div class="ct"><!-- pattern markup --></div>
  <footer class="foot">
    <span class="brand"><!-- mark + name --></span>
    <span class="pg num">02 / 08</span>
  </footer>
</section>
```

- Logo / brand sits in the **footer**, not the header (covers excepted).
- Page number uses `.pg` (coral rule before the digits).
- Speaker notes: `<aside class="notes">…</aside>` inside the slide; `N` toggles the panel.

---

## Patterns (see `examples/`)

| Pattern | Classes | Use for |
|---|---|---|
| Dark cover | `.cover .word .tagline .meta` | Title slide |
| Numbered chain + panel | `.chain` + `.panel` | Problem / narrative + proof number |
| Key rows + quote | `.rows` + `.panel.quote` | ICP / insight + pull quote |
| Process steps | `.steps` + `.step` | 3-step solution or 4-step plan |
| Stats strip | `.strip` + `.cell` / `.cell.acc` | Traction / results |
| Comparison table | `.tbl` + `.hdr.us` / `.us` | Competitive matrix |
| Pricing tiers | `.tiers` | Business model |
| Stack bands | `.stack` + `.band-item` | Product layers |
| Callout | `.callout` | Trust line / why-now |
| Fact row | `.facts` | Closing proof chips |
| Close line | `.close-line` | Sign-off |

Prefer these over inventing new card styles.

---

## Accent grammar

- **Top rule** (4px) on a panel = “this is the proof object”
- **Left bar** (6px) on a quote / callout = “listen to this”
- **Inset ring** on `.cell.acc` or `.step.last` = “this cell is the one”
- **Accent fill** on a table header / band = “this is us / the chosen column”

Reserve accent fill for one focal object per slide.

---

## Do / don’t

**Do**

- One idea per slide; size follows content
- Light first; dark only for covers / intentional interstitial
- Replace `assets/mark.svg` with the real mark; place it, don’t rebuild it
- Check overflow before export (nothing past the 1920×1080 box)

**Don’t**

- Bullet soup (five equal bullets)
- Cards around every block
- Purple / indigo gradients, glass, glow, emoji as icons
- Putting the logo in the top-left of every slide
- Shrinking type to fit — cut copy instead

---

## Presenter controls

| Key | Action |
|---|---|
| ← → / Space / Enter | Prev / next |
| N | Notes panel |
| F | Fullscreen |
| Home / End | First / last |
| `#3` in URL | Jump to slide 3 |

---

## Export

Print / PDF at **1920 × 1080** with background graphics on. `print.css` stacks every `.slide` as its own page. Puppeteer / Chromium `page.pdf({ width: '1920px', height: '1080px', printBackground: true })` is the usual path.
