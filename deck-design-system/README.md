# Deck design system

Self-contained kit for **1920 × 1080 HTML pitch decks** (and any related slide deck). Brand-agnostic: tokens, chrome, components, fonts, and examples only — no product or company context.

Open `examples/sample-deck.html` in a browser to see the system. Read `DESIGN.md` before authoring.

## Layout

```
deck-design-system/
  DESIGN.md              ← visual contract (tokens, type, patterns, rules)
  README.md
  css/
    deck.css             ← import this one file from a deck
    fonts.css
    tokens.css           ← override :root to rebrand
    base.css             ← slide / header / footer / notes
    components.css       ← cover, chain, panel, steps, strip, table, …
    print.css
  js/deck.js             ← ←/→ · N notes · F fullscreen
  fonts/                 ← Space Grotesk, Geist, Geist Mono
  assets/mark.svg        ← placeholder mark (replace)
  examples/
    sample-deck.html     ← multi-slide walkthrough of every pattern
    starter.html         ← minimal blank deck to copy
```

## Quick start

1. Copy `examples/starter.html` (or `sample-deck.html`).
2. Replace the brand name, mark (`assets/mark.svg`), and copy.
3. Keep the chrome (`.hd` / `.ct` / `.foot`) and pick patterns from `components.css`.
4. Present in the browser, or print/PDF at 1920×1080 with backgrounds on.

```html
<link rel="stylesheet" href="../css/deck.css">
…
<script src="../js/deck.js"></script>
```

## Rebrand

Override tokens — do not fork the CSS:

```css
:root {
  --accent: #2F6FED;
  --accent-deep: #1A4BB8;
  --accent-soft: #EAF1FE;
  --cover: #0B1220;
}
```

Swap fonts in `fonts.css` if the brand face differs; keep the **roles** (`--display`, `--sans`, `--mono`).

## For another AI

Hand this folder over as the only design input:

1. Read `DESIGN.md` end to end.
2. Open `examples/sample-deck.html` and match its structure.
3. Author new slides by composing existing component classes — do not invent a second motif, palette, or type stack.
4. Keep all content inside the safe zones. One idea per slide.
5. Use only the copy supplied in the brief; examples use fictional placeholder content.

## Presenter keys

| Key | Action |
|---|---|
| ← → Space Enter | Navigate |
| N | Speaker notes |
| F | Fullscreen |
